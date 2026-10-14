import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from backend.app.database import get_db
from backend.app.models.curriculum import GrammarLesson
from backend.app.models.user import User
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/grammar", tags=["Grammar"])

class GrammarLessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    category: str
    summary: Optional[str] = None
    order_index: int

class GrammarLessonDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    category: str
    summary: Optional[str] = None
    rules_markdown: str
    tables_json: Optional[str] = None
    examples_json: Optional[str] = None
    order_index: int

@router.get("/lessons", response_model=List[GrammarLessonSummary])
def get_grammar_lessons(
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(GrammarLesson)
    if level:
        query = query.filter(GrammarLesson.level == level)
    return query.order_by(GrammarLesson.order_index).all()

@router.get("/lesson/{lesson_id}", response_model=GrammarLessonDetail)
def get_grammar_lesson_detail(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lesson = db.query(GrammarLesson).filter(GrammarLesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Grammar lesson not found")
    return lesson
