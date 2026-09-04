from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models.interview import (
    Interview,
    InterviewQuestion,
    InterviewAnswer,
    InterviewEvaluation,
)

from app.services.interview_question_service import (
    generate_interview_question,
)

from app.services.evaluation_service import (
    evaluate_interview_answer,
)


class InterviewSession:
    """
    Manages one interview session.

    PostgreSQL is the permanent source of truth.

    InterviewSession connects:

        FastAPI
            ↓
        InterviewSession
            ↓
        Question Generator
            ↓
        Evaluation Service
            ↓
        PostgreSQL
    """

    # ========================================================
    # CREATE NEW INTERVIEW
    # ========================================================

    def __init__(
        self,
        db: Session,
        resume_query: str,
        job_description: str,
    ):
        """
        Create a new interview.
        """

        self.db = db

        self.resume_query = resume_query
        self.job_description = job_description

        # ----------------------------------------------------
        # Create database interview
        # ----------------------------------------------------

        interview = Interview(
            id=uuid4(),
            resume_query=resume_query,
            job_description=job_description,
            status="active",
        )

        self.db.add(interview)

        self.db.commit()

        self.db.refresh(interview)

        self.interview = interview

        self.interview_id = interview.id

        # ----------------------------------------------------
        # Runtime collections
        # ----------------------------------------------------

        self.questions = []

        self.answers = []

        self.evaluations = []

    # ========================================================
    # LOAD EXISTING INTERVIEW
    # ========================================================

    @classmethod
    def from_database(
        cls,
        db: Session,
        interview_id: UUID,
    ):
        """
        Load an existing interview from PostgreSQL.
        """

        interview = (
            db.query(Interview)
            .filter(
                Interview.id == interview_id
            )
            .first()
        )

        if interview is None:

            raise ValueError(
                f"Interview {interview_id} not found."
            )

        # ----------------------------------------------------
        # Create object without creating new database record
        # ----------------------------------------------------

        session = cls.__new__(cls)

        session.db = db

        session.interview = interview

        session.interview_id = interview.id

        session.resume_query = interview.resume_query

        session.job_description = (
            interview.job_description
        )

        # ----------------------------------------------------
        # Load questions
        # ----------------------------------------------------

        session.questions = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id
                == interview_id
            )
            .order_by(
                InterviewQuestion.question_number
            )
            .all()
        )

        # ----------------------------------------------------
        # Load answers
        # ----------------------------------------------------

        session.answers = []

        for question in session.questions:

            if question.answer is not None:

                session.answers.append(
                    question.answer
                )

        # ----------------------------------------------------
        # Load evaluations
        # ----------------------------------------------------

        session.evaluations = []

        for answer in session.answers:

            if answer.evaluation is not None:

                session.evaluations.append(
                    answer.evaluation
                )

        return session

    # ========================================================
    # BUILD CONVERSATION HISTORY
    # ========================================================

    def _build_conversation_history(self) -> str:
        """
        Convert previous questions and answers into
        conversation text.
        """

        history = []

        for question in self.questions:

            history.append(
                f"Interviewer: {question.question}"
            )

            if question.answer is not None:

                history.append(
                    f"Candidate: {question.answer.answer}"
                )

        return "\n".join(history)

    # ========================================================
    # GET QUESTIONS ASKED
    # ========================================================

    def _get_questions_asked(self) -> list[str]:
        """
        Return all questions asked so far.
        """

        return [
            question.question
            for question in self.questions
        ]

    # ========================================================
    # GET LATEST ANSWER
    # ========================================================

    def _get_latest_answer(self) -> str:
        """
        Return the latest candidate answer.
        """

        if not self.answers:

            return ""

        return self.answers[-1].answer

    # ========================================================
    # GET LATEST EVALUATION
    # ========================================================

    def _get_latest_evaluation(self) -> str:
        """
        Convert the latest evaluation into text
        for the question generator.
        """

        if not self.evaluations:

            return ""

        evaluation = self.evaluations[-1]

        return (
            f"Score: {evaluation.score}\n"
            f"Technical Accuracy: "
            f"{evaluation.technical_accuracy}\n"
            f"Relevance: "
            f"{evaluation.relevance}\n"
            f"Strengths: "
            f"{evaluation.strengths}\n"
            f"Weaknesses: "
            f"{evaluation.weaknesses}\n"
            f"Improvement: "
            f"{evaluation.improvement}\n"
            f"Follow-up Needed: "
            f"{evaluation.follow_up_needed}"
        )

    # ========================================================
    # GENERATE NEXT QUESTION
    # ========================================================

    def get_next_question(self) -> str:
        """
        Generate and save the next interview question.

        Q1 is guaranteed to be the introduction question.

        Later questions use:

        - Resume
        - Job description
        - Previous conversation
        - Previous questions
        - Latest answer
        - Latest evaluation
        - Topic rotation
        """

        # ----------------------------------------------------
        # Build context
        # ----------------------------------------------------

        conversation_history = (
            self._build_conversation_history()
        )

        questions_asked = (
            self._get_questions_asked()
        )

        latest_answer = (
            self._get_latest_answer()
        )

        evaluation_context = (
            self._get_latest_evaluation()
        )

        # ----------------------------------------------------
        # Generate question
        # ----------------------------------------------------

        question_text = generate_interview_question(
            query=self.resume_query,
            job_description=self.job_description,
            conversation_history=conversation_history,
            questions_asked=questions_asked,
            latest_answer=latest_answer,
            evaluation_context=evaluation_context,
        )

        # ----------------------------------------------------
        # Question number
        # ----------------------------------------------------

        question_number = (
            len(self.questions) + 1
        )

        # ----------------------------------------------------
        # Save question
        # ----------------------------------------------------

        question = InterviewQuestion(
            id=uuid4(),
            interview_id=self.interview_id,
            question_number=question_number,
            question=question_text,
        )

        self.db.add(question)

        self.db.commit()

        self.db.refresh(question)

        self.questions.append(question)

        return question.question

    # ========================================================
    # SAVE CANDIDATE ANSWER
    # ========================================================

    def add_candidate_answer(
        self,
        answer_text: str,
    ):
        """
        Save candidate answer and evaluate it.
        """

        # ----------------------------------------------------
        # Validate answer
        # ----------------------------------------------------

        if not answer_text or not answer_text.strip():

            raise ValueError(
                "Candidate answer cannot be empty."
            )

        # ----------------------------------------------------
        # Make sure a question exists
        # ----------------------------------------------------

        if not self.questions:

            raise ValueError(
                "There is no interview question to answer."
            )

        # ----------------------------------------------------
        # Latest question
        # ----------------------------------------------------

        question = self.questions[-1]

        # ----------------------------------------------------
        # Prevent duplicate answers
        # ----------------------------------------------------

        if question.answer is not None:

            raise ValueError(
                "This question already has an answer."
            )

        # ----------------------------------------------------
        # Create answer
        # ----------------------------------------------------

        answer = InterviewAnswer(
            id=uuid4(),
            question_id=question.id,
            answer=answer_text.strip(),
        )

        self.db.add(answer)

        self.db.commit()

        self.db.refresh(answer)

        self.answers.append(answer)

        # ----------------------------------------------------
        # Evaluate answer
        # ----------------------------------------------------

        evaluation_result = (
            evaluate_interview_answer(
                question=question.question,
                answer=answer_text,
            )
        )

        # ----------------------------------------------------
        # Support both:
        #
        # 1. Pydantic/model result
        # 2. Dictionary result
        #
        # This prevents the previous:
        #
        # AttributeError:
        # 'dict' object has no attribute 'strengths'
        # ----------------------------------------------------

        if isinstance(
            evaluation_result,
            dict,
        ):

            score = evaluation_result.get(
                "score",
                0,
            )

            technical_accuracy = (
                evaluation_result.get(
                    "technical_accuracy",
                    "",
                )
            )

            relevance = (
                evaluation_result.get(
                    "relevance",
                    "",
                )
            )

            strengths_value = (
                evaluation_result.get(
                    "strengths",
                    [],
                )
            )

            weaknesses_value = (
                evaluation_result.get(
                    "weaknesses",
                    [],
                )
            )

            improvement = (
                evaluation_result.get(
                    "improvement",
                    "",
                )
            )

            follow_up_needed = (
                evaluation_result.get(
                    "follow_up_needed",
                    False,
                )
            )

        else:

            score = evaluation_result.score

            technical_accuracy = (
                evaluation_result.technical_accuracy
            )

            relevance = (
                evaluation_result.relevance
            )

            strengths_value = (
                evaluation_result.strengths
            )

            weaknesses_value = (
                evaluation_result.weaknesses
            )

            improvement = (
                evaluation_result.improvement
            )

            follow_up_needed = (
                evaluation_result.follow_up_needed
            )

        # ----------------------------------------------------
        # Convert strengths to string
        # ----------------------------------------------------

        if isinstance(
            strengths_value,
            list,
        ):

            strengths = "\n".join(
                str(item)
                for item in strengths_value
            )

        else:

            strengths = str(
                strengths_value
            )

        # ----------------------------------------------------
        # Convert weaknesses to string
        # ----------------------------------------------------

        if isinstance(
            weaknesses_value,
            list,
        ):

            weaknesses = "\n".join(
                str(item)
                for item in weaknesses_value
            )

        else:

            weaknesses = str(
                weaknesses_value
            )

        # ----------------------------------------------------
        # Save evaluation
        # ----------------------------------------------------

        evaluation = InterviewEvaluation(
            id=uuid4(),
            answer_id=answer.id,
            score=int(score),
            technical_accuracy=str(
                technical_accuracy
            ),
            relevance=str(
                relevance
            ),
            strengths=strengths,
            weaknesses=weaknesses,
            improvement=str(
                improvement
            ),
            follow_up_needed=bool(
                follow_up_needed
            ),
        )

        self.db.add(evaluation)

        self.db.commit()

        self.db.refresh(evaluation)

        self.evaluations.append(evaluation)

        return evaluation

    # ========================================================
    # GET CURRENT INTERVIEW STATE
    # ========================================================

    def get_interview_state(self):
        """
        Return the current interview state.
        """

        return {
            "interview_id": str(
                self.interview_id
            ),

            "status": self.interview.status,

            "resume_query": (
                self.resume_query
            ),

            "job_description": (
                self.job_description
            ),

            "questions": [
                {
                    "id": str(
                        question.id
                    ),

                    "question_number": (
                        question.question_number
                    ),

                    "question": (
                        question.question
                    ),

                    "answered": (
                        question.answer is not None
                    ),
                }

                for question in self.questions
            ],

            "answers": [
                {
                    "id": str(
                        answer.id
                    ),

                    "question_id": str(
                        answer.question_id
                    ),

                    "answer": answer.answer,
                }

                for answer in self.answers
            ],

            "evaluations": [
                {
                    "id": str(
                        evaluation.id
                    ),

                    "answer_id": str(
                        evaluation.answer_id
                    ),

                    "score": evaluation.score,

                    "technical_accuracy": (
                        evaluation.technical_accuracy
                    ),

                    "relevance": (
                        evaluation.relevance
                    ),

                    "strengths": (
                        evaluation.strengths
                    ),

                    "weaknesses": (
                        evaluation.weaknesses
                    ),

                    "improvement": (
                        evaluation.improvement
                    ),

                    "follow_up_needed": (
                        evaluation.follow_up_needed
                    ),
                }

                for evaluation in self.evaluations
            ],
        }