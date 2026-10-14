import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from backend.app.database import get_db
from backend.app.models.curriculum import WritingPrompt
from backend.app.models.user import User
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/writing", tags=["Writing & Sentence Building"])

class WritingPromptSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    level: str
    category: str
    task_prompt: str
    starter_words_json: Optional[str] = None
    order_index: int

class WritingSubmission(BaseModel):
    prompt_id: int
    user_text: str

@router.get("/prompts", response_model=List[WritingPromptSummary])
def get_writing_prompts(
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(WritingPrompt)
    if level:
        query = query.filter(WritingPrompt.level == level)
    return query.order_by(WritingPrompt.order_index).all()

@router.post("/evaluate")
def evaluate_writing(
    sub: WritingSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = db.query(WritingPrompt).filter(WritingPrompt.id == sub.prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Writing prompt not found")

    user_clean = sub.user_text.strip().lower()
    solution_clean = prompt.sample_solution.strip().lower()

    # Exact or high keyword overlap
    words_expected = [w.strip(".,!?;:\"'") for w in solution_clean.split()]
    words_user = [w.strip(".,!?;:\"'") for w in user_clean.split()]

    matches = sum(1 for w in words_expected if w in words_user)
    similarity = int((matches / max(len(words_expected), 1)) * 100)

    is_perfect = (user_clean == solution_clean)
    xp_earned = 25 if (is_perfect or similarity >= 80) else 15
    current_user.xp += xp_earned
    db.commit()

    return {
        "prompt_id": prompt.id,
        "is_perfect": is_perfect,
        "similarity_score": similarity,
        "sample_solution": prompt.sample_solution,
        "xp_awarded": xp_earned,
        "feedback": "Ottimo lavoro! La tua frase è molto accurata." if similarity >= 70 else "Buon tentativo! Confronta la tua risposta con la soluzione modello."
    }
