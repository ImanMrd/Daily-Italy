import json
from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.curriculum import Exercise, Lesson
from backend.app.models.progress import UserLessonProgress, UserProgress
from backend.app.models.user import User
from backend.app.schemas import (
    ExerciseOut, LessonSubmission, LessonResultOut, ExerciseEvaluation,
    CheckAnswerRequest, CheckAnswerResponse
)
from backend.app.services.auth_service import get_optional_user

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/lesson/{lesson_id}", response_model=List[ExerciseOut])
def get_exercises_for_lesson(lesson_id: int, db: Session = Depends(get_db)):
    exercises = db.query(Exercise).filter(Exercise.lesson_id == lesson_id).all()
    return exercises

@router.post("/check-answer", response_model=CheckAnswerResponse)
def check_single_answer(req: CheckAnswerRequest, db: Session = Depends(get_db)):
    ex = db.query(Exercise).filter(Exercise.id == req.exercise_id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    user_ans = req.user_answer.strip().lower()
    corr_ans = ex.correct_answer.strip().lower()
    is_correct = (user_ans == corr_ans)

    return CheckAnswerResponse(
        exercise_id=ex.id,
        correct=is_correct,
        correct_answer=ex.correct_answer,
        explanation=ex.explanation
    )

@router.post("/submit", response_model=LessonResultOut)
def submit_lesson_exercises(
    submission: LessonSubmission,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    exercises = db.query(Exercise).filter(Exercise.lesson_id == submission.lesson_id).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found for this lesson")

    exercise_map = {ex.id: ex for ex in exercises}
    evaluations = []
    correct_count = 0

    for sub in submission.submissions:
        ex = exercise_map.get(sub.exercise_id)
        if not ex:
            continue
        
        # Normalize comparison (case-insensitive, trimmed)
        user_ans = sub.user_answer.strip().lower()
        corr_ans = ex.correct_answer.strip().lower()
        is_correct = (user_ans == corr_ans)
        
        if is_correct:
            correct_count += 1
        
        evaluations.append(ExerciseEvaluation(
            exercise_id=ex.id,
            correct=is_correct,
            user_answer=sub.user_answer,
            correct_answer=ex.correct_answer,
            explanation=ex.explanation
        ))

    total = len(exercises)
    score_percentage = int((correct_count / total) * 100) if total > 0 else 0
    xp_earned = 10 + (correct_count * 5)
    streak_updated = False
    current_streak = 1
    new_hearts = 5

    if current_user:
        current_user.xp += xp_earned
        today_str = date.today().isoformat()
        if current_user.last_active_date != today_str:
            current_user.last_active_date = today_str
            current_user.streak_days += 1
            streak_updated = True

        current_streak = current_user.streak_days

        # Check Hearts
        if score_percentage < 60:
            current_user.hearts = max(0, current_user.hearts - 1)
        elif score_percentage == 100 and current_user.hearts < 5:
            current_user.hearts = min(5, current_user.hearts + 1)

        new_hearts = current_user.hearts

        # Record user lesson progress
        prog = db.query(UserLessonProgress).filter(
            UserLessonProgress.user_id == current_user.id,
            UserLessonProgress.lesson_id == submission.lesson_id
        ).first()

        passed = (score_percentage >= 70)
        if not prog:
            prog = UserLessonProgress(
                user_id=current_user.id,
                lesson_id=submission.lesson_id,
                completed=passed,
                score_percentage=score_percentage,
                last_completed_at=datetime.utcnow()
            )
            db.add(prog)
        else:
            prog.score_percentage = max(prog.score_percentage, score_percentage)
            if passed:
                prog.completed = True
            prog.last_completed_at = datetime.utcnow()

        db.commit()

    return LessonResultOut(
        lesson_id=submission.lesson_id,
        total=total,
        correct_count=correct_count,
        score_percentage=score_percentage,
        xp_awarded=xp_earned,
        streak_updated=streak_updated,
        current_streak=current_streak,
        new_hearts=new_hearts,
        evaluations=evaluations
    )

