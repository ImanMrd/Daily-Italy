from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, ConfigDict

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[str] = None
    role: str = "user"
    xp: int
    streak_days: int
    last_active_date: Optional[str] = None
    hearts: int
    gems: int
    unlocked_levels: str = "A1"
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TokenData(BaseModel):
    username: Optional[str] = None


# Word Schemas
class WordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    italian: str
    word_type: Optional[str] = None
    english: str
    pronunciation: Optional[str] = None
    example_it: Optional[str] = None
    example_en: Optional[str] = None
    related_words: Optional[str] = None

class WordCreate(BaseModel):
    lesson_id: int
    italian: str
    word_type: Optional[str] = None
    english: str
    pronunciation: Optional[str] = None
    example_it: Optional[str] = None
    example_en: Optional[str] = None
    related_words: Optional[str] = None

# Exercise Schemas
class ExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    exercise_type: str
    prompt: str
    options_json: Optional[str] = None
    explanation: Optional[str] = None

class ExerciseSubmissionItem(BaseModel):
    exercise_id: int
    user_answer: str

class LessonSubmission(BaseModel):
    lesson_id: int
    submissions: List[ExerciseSubmissionItem]

class ExerciseEvaluation(BaseModel):
    exercise_id: int
    correct: bool
    user_answer: str
    correct_answer: str
    explanation: Optional[str] = None

class CheckAnswerRequest(BaseModel):
    exercise_id: int
    user_answer: str

class CheckAnswerResponse(BaseModel):
    exercise_id: int
    correct: bool
    correct_answer: str
    explanation: Optional[str] = None

class ExerciseCreate(BaseModel):
    lesson_id: int
    exercise_type: str
    prompt: str
    options_json: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None

class UserRoleUpdate(BaseModel):
    user_id: int
    role: str

class LessonResultOut(BaseModel):
    lesson_id: int
    total: int
    correct_count: int
    score_percentage: int
    xp_awarded: int
    streak_updated: bool
    current_streak: int
    new_hearts: int
    evaluations: List[ExerciseEvaluation]


# Spaced Repetition (SRS) Review Schemas
class FlashcardReviewSubmit(BaseModel):
    word_id: int
    # rating: 1 = Again (failed), 2 = Hard, 3 = Good, 4 = Easy
    rating: int

class SrsReviewOut(BaseModel):
    word_id: int
    next_review: datetime
    interval_days: int
    mastery_status: str

# Curriculum Tree Schemas
class LessonSummary(BaseModel):
    id: int
    title: str
    order_index: int
    word_count: int
    completed: bool = False
    score_percentage: int = 0

class UnitSummary(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    grammar_title: Optional[str] = None
    grammar_tip: Optional[str] = None
    order_index: int
    lessons: List[LessonSummary] = []

class StageSummary(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    level: str
    order_index: int
    units: List[UnitSummary] = []

# Leaderboard & Stats
class LeaderboardUser(BaseModel):
    username: str
    xp: int
    streak_days: int
    mastered_count: int

class UserStats(BaseModel):
    xp: int
    streak_days: int
    hearts: int
    gems: int
    words_learning: int
    words_mastered: int
    total_words: int
    lessons_completed: int
