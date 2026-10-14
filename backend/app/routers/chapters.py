import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from backend.app.database import get_db
from backend.app.models.curriculum import Chapter, Word, Exercise, PlacementTest
from backend.app.models.progress import UserChapterProgress
from backend.app.models.user import User
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/chapters", tags=["Chapters & Level Progression"])

# -----------------
# Schemas
# -----------------
class ChapterSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    level: str
    chapter_number: int
    title: str
    description: Optional[str] = None
    is_unlocked: bool = False
    is_completed: bool = False
    vocab_done: bool = False
    grammar_done: bool = False
    reading_done: bool = False
    writing_done: bool = False

class LevelOverview(BaseModel):
    level: str
    total_chapters: int
    completed_chapters: int
    is_unlocked: bool
    requires_placement: bool = False
    chapters: List[ChapterSummary]

class ChapterDetail(BaseModel):
    id: int
    level: str
    chapter_number: int
    title: str
    description: Optional[str] = None
    
    # Parts
    grammar_title: Optional[str] = None
    grammar_rules: Optional[str] = None
    grammar_tables: List[Dict[str, Any]] = []
    
    reading_title: Optional[str] = None
    reading_it: Optional[str] = None
    reading_en: Optional[str] = None
    reading_questions: List[Dict[str, Any]] = []
    
    writing_prompt: Optional[str] = None
    writing_starter_words: List[str] = []
    writing_sample_solution: Optional[str] = None
    
    words: List[Dict[str, Any]] = []
    exercises: List[Dict[str, Any]] = []
    
    # Progress
    vocab_done: bool = False
    grammar_done: bool = False
    reading_done: bool = False
    writing_done: bool = False
    is_completed: bool = False

class CompletePartRequest(BaseModel):
    part: str  # "vocab", "grammar", "reading", "writing", "all"
    answers: Optional[Dict[str, str]] = None
    writing_text: Optional[str] = None

class PlacementTestOut(BaseModel):
    target_level: str
    title: str
    description: Optional[str] = None
    passing_score: int
    questions: List[Dict[str, Any]]

class PlacementSubmitRequest(BaseModel):
    answers: Dict[str, str]  # { "0": "answer", ... }

class PlacementSubmitResponse(BaseModel):
    target_level: str
    passed: bool
    score: int
    passing_score: int
    correct_count: int
    total_questions: int
    message: str
    evaluations: List[Dict[str, Any]]


# -----------------
# Endpoints
# -----------------
@router.get("/overview", response_model=List[LevelOverview])
def get_curriculum_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns levels A1 (10 ch), A2 (10 ch), B1 (20 ch), B2 (20 ch).
    Sequential unlocking: Chapter 1 is open. Chapter N unlocks when Chapter N-1 is completed.
    Level unlocking: A1 is always unlocked. A2/B1/B2 are unlocked if in user.unlocked_levels.
    """
    unlocked_levels = set([lvl.strip().upper() for lvl in (current_user.unlocked_levels or "A1").split(",")])

    # Fetch user chapter progress
    user_prog_list = db.query(UserChapterProgress).filter(
        UserChapterProgress.user_id == current_user.id
    ).all()
    prog_map = {p.chapter_id: p for p in user_prog_list}

    all_chapters = db.query(Chapter).order_by(Chapter.order_index).all()
    
    # Group by level
    levels_data = [
        {"level": "A1", "total": 10},
        {"level": "A2", "total": 10},
        {"level": "B1", "total": 20},
        {"level": "B2", "total": 20}
    ]

    result = []
    for l_info in levels_data:
        lvl = l_info["level"]
        is_lvl_unlocked = (lvl in unlocked_levels)
        lvl_chapters = [ch for ch in all_chapters if ch.level == lvl]

        ch_summaries = []
        completed_count = 0

        for idx, ch in enumerate(lvl_chapters):
            p = prog_map.get(ch.id)
            is_comp = bool(p and p.completed)
            if is_comp:
                completed_count += 1

            # Chapter unlocking: First chapter of an unlocked level is open.
            # Next chapters require the previous chapter to be completed!
            if not is_lvl_unlocked:
                is_unlocked = False
            else:
                if idx == 0:
                    is_unlocked = True
                else:
                    prev_ch = lvl_chapters[idx - 1]
                    prev_prog = prog_map.get(prev_ch.id)
                    is_unlocked = bool(prev_prog and prev_prog.completed)

            ch_summaries.append(ChapterSummary(
                id=ch.id,
                level=ch.level,
                chapter_number=ch.chapter_number,
                title=ch.title,
                description=ch.description,
                is_unlocked=is_unlocked,
                is_completed=is_comp,
                vocab_done=bool(p and p.vocab_done),
                grammar_done=bool(p and p.grammar_done),
                reading_done=bool(p and p.reading_done),
                writing_done=bool(p and p.writing_done)
            ))

        result.append(LevelOverview(
            level=lvl,
            total_chapters=l_info["total"],
            completed_chapters=completed_count,
            is_unlocked=is_lvl_unlocked,
            requires_placement=(not is_lvl_unlocked),
            chapters=ch_summaries
        ))

    return result


@router.get("/chapter/{chapter_id}", response_model=ChapterDetail)
def get_chapter_detail(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ch = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Check level permission
    unlocked_levels = set([lvl.strip().upper() for lvl in (current_user.unlocked_levels or "A1").split(",")])
    if ch.level.upper() not in unlocked_levels:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Level {ch.level} is locked. Please pass the {ch.level} Placement Test or complete the previous level."
        )

    # Check sequential chapter permission
    if ch.chapter_number > 1:
        prev_ch = db.query(Chapter).filter(
            Chapter.level == ch.level,
            Chapter.chapter_number == ch.chapter_number - 1
        ).first()
        if prev_ch:
            prev_prog = db.query(UserChapterProgress).filter(
                UserChapterProgress.user_id == current_user.id,
                UserChapterProgress.chapter_id == prev_ch.id,
                UserChapterProgress.completed == True
            ).first()
            if not prev_prog:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Chapter {ch.chapter_number} is locked. You must complete Chapter {ch.chapter_number - 1} first."
                )

    # Fetch progress
    prog = db.query(UserChapterProgress).filter(
        UserChapterProgress.user_id == current_user.id,
        UserChapterProgress.chapter_id == ch.id
    ).first()

    # Parse JSON fields
    tables = []
    if ch.grammar_tables_json:
        try:
            tables = json.loads(ch.grammar_tables_json)
        except Exception:
            pass

    reading_questions = []
    if ch.reading_questions_json:
        try:
            reading_questions = json.loads(ch.reading_questions_json)
        except Exception:
            pass

    writing_chips = []
    if ch.writing_starter_words_json:
        try:
            writing_chips = json.loads(ch.writing_starter_words_json)
        except Exception:
            pass

    words_data = [
        {
            "id": w.id,
            "italian": w.italian,
            "word_type": w.word_type or "Word",
            "english": w.english,
            "pronunciation": w.pronunciation or "",
            "example_it": w.example_it or "",
            "example_en": w.example_en or "",
            "related_words": w.related_words or ""
        }
        for w in ch.words
    ]

    exercises_data = [
        {
            "id": ex.id,
            "exercise_type": ex.exercise_type,
            "prompt": ex.prompt,
            "options": json.loads(ex.options_json) if ex.options_json else [],
            "explanation": ex.explanation or ""
        }
        for ex in ch.exercises
    ]

    return ChapterDetail(
        id=ch.id,
        level=ch.level,
        chapter_number=ch.chapter_number,
        title=ch.title,
        description=ch.description,
        grammar_title=ch.grammar_title,
        grammar_rules=ch.grammar_rules,
        grammar_tables=tables,
        reading_title=ch.reading_title,
        reading_it=ch.reading_it,
        reading_en=ch.reading_en,
        reading_questions=reading_questions,
        writing_prompt=ch.writing_prompt,
        writing_starter_words=writing_chips,
        writing_sample_solution=ch.writing_sample_solution,
        words=words_data,
        exercises=exercises_data,
        vocab_done=bool(prog and prog.vocab_done),
        grammar_done=bool(prog and prog.grammar_done),
        reading_done=bool(prog and prog.reading_done),
        writing_done=bool(prog and prog.writing_done),
        is_completed=bool(prog and prog.completed)
    )


@router.post("/chapter/{chapter_id}/complete-part")
def complete_chapter_part(
    chapter_id: int,
    req: CompletePartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ch = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")

    prog = db.query(UserChapterProgress).filter(
        UserChapterProgress.user_id == current_user.id,
        UserChapterProgress.chapter_id == ch.id
    ).first()

    if not prog:
        prog = UserChapterProgress(
            user_id=current_user.id,
            chapter_id=ch.id
        )
        db.add(prog)

    part = req.part.lower()
    if part == "vocab":
        prog.vocab_done = True
        current_user.xp += 10
    elif part == "grammar":
        prog.grammar_done = True
        current_user.xp += 15
    elif part == "reading":
        # Strictly validate reading questions if defined
        if ch.reading_questions_json:
            try:
                rq_list = json.loads(ch.reading_questions_json)
            except Exception:
                rq_list = []
            if rq_list:
                if not req.answers:
                    raise HTTPException(
                        status_code=400,
                        detail="Please answer all reading comprehension questions before marking this section complete."
                    )
                for idx, q in enumerate(rq_list):
                    user_ans = (req.answers.get(str(idx)) or req.answers.get(idx) or "").strip().lower()
                    corr_ans = (q.get("correct_answer") or "").strip().lower()
                    if not user_ans:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Question {idx+1} is unanswered. Please answer all questions."
                        )
                    if user_ans != corr_ans:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Answer for Question {idx+1} is incorrect. Please review the text and select the correct answer."
                        )
        prog.reading_done = True
        current_user.xp += 20
    elif part == "writing":
        # Strictly validate that writing is not empty and has substantive content
        w_text = (req.writing_text or "").strip()
        words = [w for w in w_text.split() if w]
        if len(w_text) < 10 or len(words) < 3:
            raise HTTPException(
                status_code=400,
                detail="Your Italian writing submission must be at least 10 characters and 3 words long. Please write your response before completing this section."
            )
        prog.writing_done = True
        current_user.xp += 25
    elif part == "all":
        prog.vocab_done = True
        prog.grammar_done = True
        prog.reading_done = True
        prog.writing_done = True

    # Check if all 4 parts are completed
    is_fully_done = (prog.vocab_done and prog.grammar_done and prog.reading_done and prog.writing_done)
    if is_fully_done and not prog.completed:
        prog.completed = True
        prog.completed_at = datetime.utcnow()
        current_user.xp += 30  # Chapter mastery bonus!

        # Check if this completion unlocks the next level!
        unlocked = set([lvl.strip().upper() for lvl in (current_user.unlocked_levels or "A1").split(",")])
        if ch.level == "A1" and ch.chapter_number == 10:
            unlocked.add("A2")
        elif ch.level == "A2" and ch.chapter_number == 10:
            unlocked.add("B1")
        elif ch.level == "B1" and ch.chapter_number == 20:
            unlocked.add("B2")
        current_user.unlocked_levels = ",".join(sorted(list(unlocked)))

    db.commit()
    db.refresh(prog)

    return {
        "chapter_id": ch.id,
        "part_completed": part,
        "vocab_done": prog.vocab_done,
        "grammar_done": prog.grammar_done,
        "reading_done": prog.reading_done,
        "writing_done": prog.writing_done,
        "chapter_completed": prog.completed,
        "user_xp": current_user.xp,
        "unlocked_levels": current_user.unlocked_levels
    }


# -----------------
# Placement Tests
# -----------------
@router.get("/placement/{level}", response_model=PlacementTestOut)
def get_placement_test(
    level: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    level_norm = level.strip().upper()
    pt = db.query(PlacementTest).filter(PlacementTest.target_level == level_norm).first()
    if not pt:
        raise HTTPException(status_code=404, detail=f"Placement test for Level {level_norm} not found")

    questions = json.loads(pt.questions_json)
    # Strip correct answers when sending to client
    sanitized_questions = []
    for q in questions:
        sanitized_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })

    return PlacementTestOut(
        target_level=pt.target_level,
        title=pt.title,
        description=pt.description,
        passing_score=pt.passing_score,
        questions=sanitized_questions
    )


@router.post("/placement/{level}/submit", response_model=PlacementSubmitResponse)
def submit_placement_test(
    level: str,
    sub: PlacementSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    level_norm = level.strip().upper()
    pt = db.query(PlacementTest).filter(PlacementTest.target_level == level_norm).first()
    if not pt:
        raise HTTPException(status_code=404, detail=f"Placement test for Level {level_norm} not found")

    questions = json.loads(pt.questions_json)
    correct_count = 0
    evaluations = []

    for idx, q in enumerate(questions):
        user_ans = sub.answers.get(str(idx), "").strip().lower()
        corr_ans = q["correct_answer"].strip().lower()
        is_corr = (user_ans == corr_ans)
        if is_corr:
            correct_count += 1
        evaluations.append({
            "question_id": q["id"],
            "question": q["question"],
            "correct": is_corr,
            "correct_answer": q["correct_answer"],
            "explanation": q.get("explanation", "")
        })

    # Each question is worth 10 points (total 100)
    score = int((correct_count / max(len(questions), 1)) * 100)
    passed = (score >= pt.passing_score)

    if passed:
        unlocked = set([lvl.strip().upper() for lvl in (current_user.unlocked_levels or "A1").split(",")])
        unlocked.add(level_norm)
        current_user.unlocked_levels = ",".join(sorted(list(unlocked)))
        current_user.xp += 50  # Placement test bonus!
        db.commit()
        message = f"Congratulations! You scored {score}/100 and successfully unlocked Level {level_norm}!"
    else:
        message = f"You scored {score}/100. A minimum of {pt.passing_score}/100 is required to skip to Level {level_norm}. Keep practicing or retake the test!"

    return PlacementSubmitResponse(
        target_level=level_norm,
        passed=passed,
        score=score,
        passing_score=pt.passing_score,
        correct_count=correct_count,
        total_questions=len(questions),
        message=message,
        evaluations=evaluations
    )
