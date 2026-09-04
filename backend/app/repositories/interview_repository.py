from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview import (
    Interview,
    InterviewQuestion,
    InterviewAnswer,
    InterviewEvaluation,
    InterviewReportDB,
)


class InterviewRepository:
    """
    Handles all PostgreSQL operations related to interviews.
    """

    def __init__(self, db: Session):
        self.db = db

    # ========================================================
    # Interview
    # ========================================================

    def create_interview(
        self,
        resume_query: str,
        job_description: str,
    ) -> Interview:
        """
        Create a new interview record.
        """

        interview = Interview(
            resume_query=resume_query,
            job_description=job_description,
            status="in_progress",
        )

        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)

        return interview

    # ========================================================
    # Get Interview
    # ========================================================

    def get_interview(
        self,
        interview_id: UUID,
    ) -> Interview | None:
        """
        Get an interview by ID.
        """

        statement = select(Interview).where(
            Interview.id == interview_id
        )

        return self.db.scalar(statement)

    # ========================================================
    # Update Interview Status
    # ========================================================

    def update_interview_status(
        self,
        interview: Interview,
        status: str,
    ) -> Interview:
        """
        Update interview status.
        """

        interview.status = status

        self.db.commit()
        self.db.refresh(interview)

        return interview

    # ========================================================
    # Question
    # ========================================================

    def create_question(
        self,
        interview_id: UUID,
        question_number: int,
        question: str,
    ) -> InterviewQuestion:
        """
        Save an interview question.
        """

        interview_question = InterviewQuestion(
            interview_id=interview_id,
            question_number=question_number,
            question=question,
        )

        self.db.add(interview_question)
        self.db.commit()
        self.db.refresh(interview_question)

        return interview_question

    # ========================================================
    # Answer
    # ========================================================

    def create_answer(
        self,
        question_id: UUID,
        answer: str,
    ) -> InterviewAnswer:
        """
        Save a candidate answer.
        """

        interview_answer = InterviewAnswer(
            question_id=question_id,
            answer=answer,
        )

        self.db.add(interview_answer)
        self.db.commit()
        self.db.refresh(interview_answer)

        return interview_answer

    # ========================================================
    # Evaluation
    # ========================================================

    def create_evaluation(
        self,
        answer_id: UUID,
        score: int,
        technical_accuracy: str,
        relevance: str,
        strengths: str,
        weaknesses: str,
        improvement: str,
        follow_up_needed: bool,
    ) -> InterviewEvaluation:
        """
        Save an answer evaluation.
        """

        evaluation = InterviewEvaluation(
            answer_id=answer_id,
            score=score,
            technical_accuracy=technical_accuracy,
            relevance=relevance,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement=improvement,
            follow_up_needed=follow_up_needed,
        )

        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)

        return evaluation

    # ========================================================
    # Final Report
    # ========================================================

    def create_report(
        self,
        interview_id: UUID,
        overall_score: float,
        technical_performance: str,
        communication: str,
        strengths: str,
        weaknesses: str,
        skills_demonstrated: str,
        skills_to_improve: str,
        job_fit: str,
        recommendations: str,
    ) -> InterviewReportDB:
        """
        Save the final interview report.
        """

        report = InterviewReportDB(
            interview_id=interview_id,
            overall_score=overall_score,
            technical_performance=technical_performance,
            communication=communication,
            strengths=strengths,
            weaknesses=weaknesses,
            skills_demonstrated=skills_demonstrated,
            skills_to_improve=skills_to_improve,
            job_fit=job_fit,
            recommendations=recommendations,
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        return report