from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.app.database import get_db
from backend.app.models.curriculum import Word
from backend.app.models.progress import UserProgress
from backend.app.models.user import User
from backend.app.schemas import FlashcardReviewSubmit, SrsReviewOut
from backend.app.services.auth_service import get_optional_user, get_current_user
from backend.app.services.srs_service import calculate_sm2

router = APIRouter(prefix="/review", tags=["Smart Review"])

@router.get("/queue")
def get_review_queue(
    limit: int = 25,
    filter_mode: Optional[str] = "all",  # "all", "weak", "due"
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    # If not logged in, return initial foundational words safely
    if not current_user:
        sample_words = db.query(Word).limit(limit).all()
        return {
            "queue_type": "guest_sample",
            "count": len(sample_words),
            "words": [
                {
                    "word_id": w.id,
                    "italian": w.italian,
                    "word_type": w.word_type or "Parola",
                    "english": w.english,
                    "pronunciation": w.pronunciation or "",
                    "example_it": w.example_it or "",
                    "example_en": w.example_en or "",
                    "related_words": w.related_words or "",
                    "mastery_status": "learning",
                    "repetitions": 0,
                    "interval_days": 1,
                    "next_review": datetime.utcnow().isoformat()
                }
                for w in sample_words
            ]
        }

    now = datetime.utcnow()
    query = db.query(UserProgress).filter(UserProgress.user_id == current_user.id)

    if filter_mode == "weak":
        query = query.filter(
            or_(
                UserProgress.mastery_status == "review_needed",
                UserProgress.times_incorrect > 0
            )
        )
    elif filter_mode == "due":
        query = query.filter(UserProgress.next_review <= now)

    progress_items = query.order_by(UserProgress.next_review.asc()).limit(limit).all()

    # If no personal progress records exist yet, provide first stage words
    if not progress_items:
        first_words = db.query(Word).limit(limit).all()
        return {
            "queue_type": "initial_study",
            "count": len(first_words),
            "words": [
                {
                    "word_id": w.id,
                    "italian": w.italian,
                    "word_type": w.word_type or "Parola",
                    "english": w.english,
                    "pronunciation": w.pronunciation or "",
                    "example_it": w.example_it or "",
                    "example_en": w.example_en or "",
                    "related_words": w.related_words or "",
                    "mastery_status": "learning",
                    "repetitions": 0,
                    "interval_days": 1,
                    "next_review": datetime.utcnow().isoformat()
                }
                for w in first_words
            ]
        }

    word_ids = [p.word_id for p in progress_items]
    words = db.query(Word).filter(Word.id.in_(word_ids)).all()
    word_dict = {w.id: w for w in words}

    items = []
    for p in progress_items:
        w = word_dict.get(p.word_id)
        if w:
            items.append({
                "word_id": w.id,
                "italian": w.italian,
                "word_type": w.word_type or "Parola",
                "english": w.english,
                "pronunciation": w.pronunciation or "",
                "example_it": w.example_it or "",
                "example_en": w.example_en or "",
                "related_words": w.related_words or "",
                "mastery_status": p.mastery_status or "learning",
                "repetitions": p.repetition or 0,
                "interval_days": p.interval_days or 1,
                "next_review": (p.next_review or now).isoformat()
            })

    return {
        "queue_type": filter_mode,
        "count": len(items),
        "words": items
    }

@router.post("/submit", response_model=SrsReviewOut)
def submit_flashcard_review(
    review_in: FlashcardReviewSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(Word.id == review_in.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    prog = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.word_id == review_in.word_id
    ).first()

    if not prog:
        prog = UserProgress(
            user_id=current_user.id,
            word_id=review_in.word_id,
            repetition=0,
            interval_days=1,
            ease_factor=2.5,
            mastery_status="learning"
        )
        db.add(prog)

    prog = calculate_sm2(prog, review_in.rating)

    xp_award = 5 if review_in.rating >= 3 else 2
    current_user.xp += xp_award

    db.commit()
    db.refresh(prog)

    return SrsReviewOut(
        word_id=prog.word_id,
        next_review=prog.next_review,
        interval_days=prog.interval_days,
        mastery_status=prog.mastery_status
    )
