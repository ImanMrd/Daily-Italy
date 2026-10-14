from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.curriculum import Word
from backend.app.models.progress import UserProgress, UserLessonProgress
from backend.app.models.user import User
from backend.app.schemas import UserStats, LeaderboardUser
from backend.app.services.auth_service import get_optional_user

router = APIRouter(prefix="/stats", tags=["Stats & Leaderboard"])

@router.get("/summary", response_model=UserStats)
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    total_words = db.query(Word).count()

    if not current_user:
        return UserStats(
            xp=0,
            streak_days=1,
            hearts=5,
            gems=50,
            words_learning=0,
            words_mastered=0,
            total_words=total_words,
            lessons_completed=0
        )

    mastered = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.mastery_status == "mastered"
    ).count()

    learning = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.mastery_status == "learning"
    ).count()

    lessons_completed = db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == current_user.id,
        UserLessonProgress.completed == True
    ).count()

    return UserStats(
        xp=current_user.xp,
        streak_days=current_user.streak_days,
        hearts=current_user.hearts,
        gems=current_user.gems,
        words_learning=learning,
        words_mastered=mastered,
        total_words=total_words,
        lessons_completed=lessons_completed
    )


@router.get("/leaderboard", response_model=List[LeaderboardUser])
def get_leaderboard(db: Session = Depends(get_db)):
    top_users = db.query(User).order_by(User.xp.desc()).limit(15).all()

    result = []
    for u in top_users:
        mastered_count = db.query(UserProgress).filter(
            UserProgress.user_id == u.id,
            UserProgress.mastery_status == "mastered"
        ).count()
        result.append(LeaderboardUser(
            username=u.username,
            xp=u.xp,
            streak_days=u.streak_days,
            mastered_count=mastered_count
        ))
    return result
