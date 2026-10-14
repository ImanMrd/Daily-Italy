from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.curriculum import Word, Lesson, Unit, Stage
from backend.app.models.user import User
from backend.app.schemas import WordOut, WordCreate
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/words", tags=["Words"])

@router.get("/lesson/{lesson_id}", response_model=List[WordOut])
def get_words_for_lesson(lesson_id: int, db: Session = Depends(get_db)):
    words = db.query(Word).filter(Word.lesson_id == lesson_id).all()
    return words

@router.post("/custom", response_model=WordOut)
def create_custom_word(
    word_in: WordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify lesson exists
    lesson = db.query(Lesson).filter(Lesson.id == word_in.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Target lesson does not exist")

    new_word = Word(
        lesson_id=word_in.lesson_id,
        italian=word_in.italian.strip(),
        word_type=word_in.word_type,
        english=word_in.english.strip(),
        pronunciation=word_in.pronunciation,
        example_it=word_in.example_it,
        example_en=word_in.example_en,
        related_words=word_in.related_words
    )
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word
