from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.curriculum import Chapter, Word, Exercise, PlacementTest
from backend.app.models.progress import UserChapterProgress
from backend.app.schemas import WordCreate, WordOut, ExerciseCreate, ExerciseOut, UserOut
from backend.app.services.auth_service import require_admin
from backend.scripts.seed_full_curriculum import seed_full_curriculum_database

router = APIRouter(prefix="/admin", tags=["RBAC Admin"])

class RoleUpdateRequest(BaseModel):
    role: str  # "admin" or "user"

class UnlockLevelRequest(BaseModel):
    level: str  # "A1", "A2", "B1", "B2"

class ThresholdUpdateRequest(BaseModel):
    passing_score: int  # e.g. 70

@router.get("/overview")
def get_admin_overview(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    total_users = db.query(User).count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    total_chapters = db.query(Chapter).count()
    total_words = db.query(Word).count()
    total_exercises = db.query(Exercise).count()
    total_tests = db.query(PlacementTest).count()
    chapter_completions = db.query(UserChapterProgress).filter(UserChapterProgress.completed == True).count()

    # Level counts
    a1_count = db.query(Chapter).filter(Chapter.level == "A1").count()
    a2_count = db.query(Chapter).filter(Chapter.level == "A2").count()
    b1_count = db.query(Chapter).filter(Chapter.level == "B1").count()
    b2_count = db.query(Chapter).filter(Chapter.level == "B2").count()

    return {
        "total_users": total_users,
        "total_admins": total_admins,
        "total_chapters": total_chapters,
        "total_words": total_words,
        "total_exercises": total_exercises,
        "total_placement_tests": total_tests,
        "total_chapter_completions": chapter_completions,
        "chapters_by_level": {
            "A1": a1_count,
            "A2": a2_count,
            "B1": b1_count,
            "B2": b2_count
        }
    }

@router.get("/users", response_model=List[UserOut])
def list_all_users(
    query: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    q = db.query(User)
    if query:
        q = q.filter(User.username.ilike(f"%{query}%"))
    return q.order_by(User.id.desc()).all()

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    req: RoleUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    if req.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'admin'")
    
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == admin.id and req.role != "admin":
        raise HTTPException(status_code=400, detail="Cannot revoke your own admin rights")

    target_user.role = req.role
    db.commit()
    return {"status": "success", "user_id": user_id, "new_role": req.role}

@router.put("/users/{user_id}/unlock-level")
def admin_unlock_user_level(
    user_id: int,
    req: UnlockLevelRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    lvl = req.level.strip().upper()
    if lvl not in ["A1", "A2", "B1", "B2"]:
        raise HTTPException(status_code=400, detail="Level must be one of: A1, A2, B1, B2")

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    current_unlocked = set([l.strip().upper() for l in (target_user.unlocked_levels or "A1").split(",")])
    current_unlocked.add(lvl)
    target_user.unlocked_levels = ",".join(sorted(list(current_unlocked)))
    db.commit()

    return {
        "status": "success",
        "user_id": user_id,
        "unlocked_levels": target_user.unlocked_levels,
        "message": f"Level {lvl} successfully unlocked for user {target_user.username}."
    }

@router.delete("/users/{user_id}")
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own admin account")

    # Delete related user progress
    db.query(UserChapterProgress).filter(UserChapterProgress.user_id == user_id).delete()
    db.delete(target_user)
    db.commit()
    return {"status": "deleted", "user_id": user_id}

@router.get("/placement-tests")
def get_admin_placement_tests(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    pts = db.query(PlacementTest).order_by(PlacementTest.target_level).all()
    return [
        {
            "id": p.id,
            "target_level": p.target_level,
            "title": p.title,
            "passing_score": p.passing_score
        }
        for p in pts
    ]

@router.put("/placement-tests/{level}/threshold")
def update_placement_threshold(
    level: str,
    req: ThresholdUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    pt = db.query(PlacementTest).filter(PlacementTest.target_level == level.upper()).first()
    if not pt:
        raise HTTPException(status_code=404, detail="Placement test not found")

    pt.passing_score = req.passing_score
    db.commit()
    return {"status": "updated", "target_level": pt.target_level, "passing_score": pt.passing_score}

@router.post("/curriculum/reseed")
def admin_reseed_curriculum(
    admin: User = Depends(require_admin)
):
    seed_full_curriculum_database()
    return {"status": "reseeded", "message": "Curriculum successfully re-seeded from resources."}
