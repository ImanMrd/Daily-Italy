from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False, index=True)

    # SuperMemo-2 / Leitner parameters
    repetition = Column(Integer, default=0)
    interval_days = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    last_reviewed = Column(DateTime, default=datetime.utcnow)
    next_review = Column(DateTime, default=datetime.utcnow)
    mastery_status = Column(String(20), default="learning")  # learning, review_needed, mastered
    times_correct = Column(Integer, default=0)
    times_incorrect = Column(Integer, default=0)

    word = relationship("Word")


class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)

    completed = Column(Boolean, default=False)
    score_percentage = Column(Integer, default=0)
    last_completed_at = Column(DateTime, default=datetime.utcnow)

    lesson = relationship("Lesson")


class UserChapterProgress(Base):
    __tablename__ = "user_chapter_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False, index=True)

    vocab_done = Column(Boolean, default=False)
    grammar_done = Column(Boolean, default=False)
    reading_done = Column(Boolean, default=False)
    writing_done = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    score_percentage = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)

    chapter = relationship("backend.app.models.curriculum.Chapter")
