import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from backend.app.database import get_db
from backend.app.models.curriculum import ReadingPassage
from backend.app.models.user import User
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/readings", tags=["Readings & Comprehension"])

class ReadingPassageSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    category: str
    order_index: int

class ReadingPassageDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    category: str
    content_it: str
    content_en: Optional[str] = None
    vocabulary_hints_json: Optional[str] = None
    questions_json: Optional[str] = None
    order_index: int

class ReadingAnswerSubmit(BaseModel):
    answers: dict  # { question_index: user_answer }

@router.get("", response_model=List[ReadingPassageSummary])
def get_reading_passages(
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ReadingPassage)
    if level:
        query = query.filter(ReadingPassage.level == level)
    return query.order_by(ReadingPassage.order_index).all()

@router.get("/{passage_id}", response_model=ReadingPassageDetail)
def get_reading_passage_detail(
    passage_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    passage = db.query(ReadingPassage).filter(ReadingPassage.id == passage_id).first()
    if not passage:
        raise HTTPException(status_code=404, detail="Reading passage not found")
    return passage

@router.post("/{passage_id}/submit")
def submit_reading_answers(
    passage_id: int,
    sub: ReadingAnswerSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    passage = db.query(ReadingPassage).filter(ReadingPassage.id == passage_id).first()
    if not passage:
        raise HTTPException(status_code=404, detail="Reading passage not found")

    questions = json.loads(passage.questions_json or "[]")
    results = []
    correct_count = 0

    for idx, q in enumerate(questions):
        user_ans = sub.answers.get(str(idx), "").strip().lower()
        corr_ans = q.get("correct_answer", "").strip().lower()
        is_corr = (user_ans == corr_ans)
        if is_corr:
            correct_count += 1
        results.append({
            "question_index": idx,
            "question": q.get("question"),
            "correct": is_corr,
            "correct_answer": q.get("correct_answer"),
            "explanation": q.get("explanation", "")
        })

    xp_earned = 15 + (correct_count * 10)
    current_user.xp += xp_earned
    db.commit()

    return {
        "passage_id": passage_id,
        "total": len(questions),
        "correct_count": correct_count,
        "xp_awarded": xp_earned,
        "evaluations": results
    }
