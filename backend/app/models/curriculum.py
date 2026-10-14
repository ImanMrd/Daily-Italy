from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    level = Column(String(10), default="A1")  # A1, A2, B1, B2, C1
    order_index = Column(Integer, default=1)

    units = relationship("Unit", back_populates="stage", cascade="all, delete-orphan", order_by="Unit.order_index")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    grammar_tip = Column(Text, nullable=True)  # Busuu-style "Nota Bene" tip before lesson
    grammar_title = Column(String(100), nullable=True)
    order_index = Column(Integer, default=1)

    stage = relationship("Stage", back_populates="units")
    lessons = relationship("Lesson", back_populates="unit", cascade="all, delete-orphan", order_by="Lesson.order_index")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    title = Column(String(150), nullable=False)
    order_index = Column(Integer, default=1)

    unit = relationship("Unit", back_populates="lessons")
    words = relationship("Word", back_populates="lesson", cascade="all, delete-orphan", order_by="Word.id")
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan", order_by="Exercise.id")


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True, index=True)
    italian = Column(String(100), nullable=False, index=True)
    word_type = Column(String(20), nullable=True)  # Va, Vr, Nm, Nf, Agg, Avv, Cong, Prep
    english = Column(String(200), nullable=False)
    pronunciation = Column(String(100), nullable=True)  # e.g., IPA or intuitive phonetic
    example_it = Column(Text, nullable=True)
    example_en = Column(Text, nullable=True)
    related_words = Column(String(255), nullable=True)  # Word family derivatives (e.g. abitare -> abitazione)
    
    lesson = relationship("Lesson", back_populates="words")
    chapter = relationship("Chapter", back_populates="words")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True, index=True)
    exercise_type = Column(String(50), nullable=False)  # multiple_choice, cloze, matching, odd_one_out
    prompt = Column(Text, nullable=False)
    options_json = Column(Text, nullable=True)  # JSON string of options or word pairs
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)

    lesson = relationship("Lesson", back_populates="exercises")
    chapter = relationship("Chapter", back_populates="exercises")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(10), nullable=False, index=True)  # A1, A2, B1, B2
    chapter_number = Column(Integer, nullable=False)        # 1..10 (A1, A2) or 1..20 (B1, B2)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    
    # Part 2: Grammar
    grammar_title = Column(String(150), nullable=True)
    grammar_rules = Column(Text, nullable=True)             # Rules in English
    grammar_tables_json = Column(Text, nullable=True)
    
    # Part 3: Reading
    reading_title = Column(String(150), nullable=True)
    reading_it = Column(Text, nullable=True)
    reading_en = Column(Text, nullable=True)
    reading_questions_json = Column(Text, nullable=True)
    
    # Part 4: Writing
    writing_prompt = Column(Text, nullable=True)
    writing_starter_words_json = Column(Text, nullable=True)
    writing_sample_solution = Column(Text, nullable=True)
    
    order_index = Column(Integer, default=1)

    words = relationship("Word", back_populates="chapter", cascade="all, delete-orphan", order_by="Word.id")
    exercises = relationship("Exercise", back_populates="chapter", cascade="all, delete-orphan", order_by="Exercise.id")


class PlacementTest(Base):
    __tablename__ = "placement_tests"

    id = Column(Integer, primary_key=True, index=True)
    target_level = Column(String(10), unique=True, index=True, nullable=False)  # A2, B1, B2
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    passing_score = Column(Integer, default=70)  # User requires 70/100 to pass
    questions_json = Column(Text, nullable=False)  # 10 questions worth 10 points each


class GrammarLesson(Base):
    __tablename__ = "grammar_lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    level = Column(String(10), default="A1")  # A1, A2, B1, B2, C1, C2
    category = Column(String(100), nullable=False)  # Nomi, Articoli, Verbi, Pronomi, etc.
    summary = Column(String(255), nullable=True)
    rules_markdown = Column(Text, nullable=False)
    tables_json = Column(Text, nullable=True)
    examples_json = Column(Text, nullable=True)
    order_index = Column(Integer, default=1)


class ReadingPassage(Base):
    __tablename__ = "reading_passages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    level = Column(String(10), default="A1")
    category = Column(String(100), default="Cultura")
    content_it = Column(Text, nullable=False)
    content_en = Column(Text, nullable=True)
    vocabulary_hints_json = Column(Text, nullable=True)
    questions_json = Column(Text, nullable=True)
    order_index = Column(Integer, default=1)


class WritingPrompt(Base):
    __tablename__ = "writing_prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    level = Column(String(10), default="A1")
    category = Column(String(100), default="Frasi & Traduzione")
    task_prompt = Column(Text, nullable=False)
    starter_words_json = Column(Text, nullable=True)
    sample_solution = Column(Text, nullable=False)
    order_index = Column(Integer, default=1)

