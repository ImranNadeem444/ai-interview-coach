from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


# ============================================================
# 1. Interview Session
# ============================================================

class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    resume_query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    questions: Mapped[list["InterviewQuestion"]] = relationship(
        back_populates="interview",
        cascade="all, delete-orphan",
    )

    report: Mapped["InterviewReportDB | None"] = relationship(
        back_populates="interview",
        cascade="all, delete-orphan",
        uselist=False,
    )


# ============================================================
# 2. Interview Question
# ============================================================

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    interview_id: Mapped[UUID] = mapped_column(
        ForeignKey("interviews.id"),
        nullable=False,
    )

    question_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    interview: Mapped["Interview"] = relationship(
        back_populates="questions",
    )

    answer: Mapped["InterviewAnswer | None"] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        uselist=False,
    )


# ============================================================
# 3. Candidate Answer
# ============================================================

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_questions.id"),
        nullable=False,
        unique=True,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    question: Mapped["InterviewQuestion"] = relationship(
        back_populates="answer",
    )

    evaluation: Mapped["InterviewEvaluation | None"] = relationship(
        back_populates="answer",
        cascade="all, delete-orphan",
        uselist=False,
    )


# ============================================================
# 4. Answer Evaluation
# ============================================================

class InterviewEvaluation(Base):
    __tablename__ = "interview_evaluations"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    answer_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_answers.id"),
        nullable=False,
        unique=True,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    technical_accuracy: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    relevance: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    strengths: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    weaknesses: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    improvement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    follow_up_needed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    answer: Mapped["InterviewAnswer"] = relationship(
        back_populates="evaluation",
    )


# ============================================================
# 5. Final Interview Report
# ============================================================

class InterviewReportDB(Base):
    __tablename__ = "interview_reports"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    interview_id: Mapped[UUID] = mapped_column(
        ForeignKey("interviews.id"),
        nullable=False,
        unique=True,
    )

    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    technical_performance: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    communication: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    strengths: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    weaknesses: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    skills_demonstrated: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    skills_to_improve: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    job_fit: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    recommendations: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    interview: Mapped["Interview"] = relationship(
        back_populates="report",
    )