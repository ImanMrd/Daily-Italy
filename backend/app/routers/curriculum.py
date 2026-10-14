from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.curriculum import Stage, Unit, Lesson, Word, Exercise
from backend.app.models.progress import UserLessonProgress
from backend.app.models.user import User
from backend.app.schemas import StageSummary, UnitSummary, LessonSummary
from backend.app.services.auth_service import get_optional_user

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])

@router.get("/stages", response_model=List[StageSummary])
def get_stages(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    stages = db.query(Stage).order_by(Stage.order_index).all()
    
    # Get user completed lessons
    completed_map = {}
    if current_user:
        user_progress = db.query(UserLessonProgress).filter(
            UserLessonProgress.user_id == current_user.id
        ).all()
        for p in user_progress:
            completed_map[p.lesson_id] = {
                "completed": p.completed,
                "score": p.score_percentage
            }

    result = []
    for stage in stages:
        stage_units = []
        for unit in stage.units:
            unit_lessons = []
            for lesson in unit.lessons:
                prog = completed_map.get(lesson.id, {"completed": False, "score": 0})
                word_count = db.query(Word).filter(Word.lesson_id == lesson.id).count()
                unit_lessons.append(LessonSummary(
                    id=lesson.id,
                    title=lesson.title,
                    order_index=lesson.order_index,
                    word_count=word_count,
                    completed=prog["completed"],
                    score_percentage=prog["score"]
                ))
            stage_units.append(UnitSummary(
                id=unit.id,
                title=unit.title,
                description=unit.description,
                grammar_title=unit.grammar_title,
                grammar_tip=unit.grammar_tip,
                order_index=unit.order_index,
                lessons=unit_lessons
            ))
        result.append(StageSummary(
            id=stage.id,
            name=stage.name,
            description=stage.description,
            level=stage.level,
            order_index=stage.order_index,
            units=stage_units
        ))
    return result

@router.get("/lesson/{lesson_id}")
def get_lesson_detail(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    words = db.query(Word).filter(Word.lesson_id == lesson_id).all()
    unit = lesson.unit

    completed = False
    score = 0
    if current_user:
        prog = db.query(UserLessonProgress).filter(
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.lesson_id == lesson_id
        ).first()
        if prog:
            completed = prog.completed
            score = prog.score_percentage

    return {
        "id": lesson.id,
        "title": lesson.title,
        "order_index": lesson.order_index,
        "unit_id": unit.id,
        "unit_title": unit.title,
        "grammar_title": unit.grammar_title,
        "grammar_tip": unit.grammar_tip,
        "words": words,
        "word_count": len(words),
        "completed": completed,
        "score_percentage": score
    }
