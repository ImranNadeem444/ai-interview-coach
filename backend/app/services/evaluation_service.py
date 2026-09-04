from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.services.llm_service import get_llm


# ============================================================
# Evaluation Result
# ============================================================

class InterviewEvaluationResult(BaseModel):
    score: int = Field(
        ge=1,
        le=10,
        description="Overall score from 1 to 10.",
    )

    technical_accuracy: str = Field(
        description="How technically correct the answer was.",
    )

    relevance: str = Field(
        description="How relevant the answer was to the question.",
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Main strengths demonstrated by the candidate.",
    )

    weaknesses: List[str] = Field(
        default_factory=list,
        description="Main weaknesses in the answer.",
    )

    improvement: str = Field(
        description="How the candidate could improve the answer.",
    )

    follow_up_needed: bool = Field(
        description="Whether a follow-up question is useful.",
    )


# ============================================================
# Parser
# ============================================================

parser = PydanticOutputParser(
    pydantic_object=InterviewEvaluationResult
)


# ============================================================
# Evaluation Prompt
# ============================================================

evaluation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert technical interviewer and AI/ML interview evaluator.

Evaluate the candidate's answer fairly and realistically.

You have:

1. The interview question
2. The candidate's answer
3. Candidate resume
4. Job description
5. Previous interview context

Evaluate the candidate based on the actual answer.

Do not give credit for technologies or experience that the
candidate did not demonstrate in the answer.

Consider:

- Technical correctness
- Understanding
- Relevance
- Clarity
- Practical experience
- Depth
- Communication

Score the answer from 1 to 10.

Scoring guide:

1-2:
Very poor or completely incorrect.

3-4:
Weak understanding with major gaps.

5-6:
Basic understanding but lacks depth.

7-8:
Good answer with solid understanding.

9:
Very strong answer with strong technical depth.

10:
Exceptional answer with excellent technical depth,
accuracy, examples, and practical understanding.

Do not be unnecessarily harsh.

If the candidate gives a short but correct answer,
evaluate what they actually said rather than penalizing
them excessively for not discussing unrelated topics.

For weaknesses, identify genuine areas that could be improved.

For improvement, give practical advice.

Set follow_up_needed to true when the answer leaves
important technical areas worth exploring.

{format_instructions}
""",
        ),
        (
            "human",
            """
============================================================
QUESTION
============================================================

{question}

============================================================
CANDIDATE ANSWER
============================================================

{answer}

============================================================
CANDIDATE RESUME
============================================================

{resume_context}

============================================================
JOB DESCRIPTION
============================================================

{job_description}

============================================================
PREVIOUS INTERVIEW CONTEXT
============================================================

{interview_history}

============================================================
TASK
============================================================

Evaluate this candidate answer.
""",
        ),
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)


# ============================================================
# Evaluation Chain
# ============================================================

def get_evaluation_chain():
    llm = get_llm()

    return (
        evaluation_prompt
        | llm
        | parser
    )


# ============================================================
# Evaluate Answer
# ============================================================

def evaluate_interview_answer(
    question: str,
    answer: str,
    resume_context: str = "",
    job_description: str = "",
    interview_history: str = "",
) -> InterviewEvaluationResult:

    if not question or not question.strip():
        raise ValueError(
            "Interview question cannot be empty."
        )

    if not answer or not answer.strip():
        raise ValueError(
            "Candidate answer cannot be empty."
        )

    chain = get_evaluation_chain()

    result = chain.invoke(
        {
            "question": question,
            "answer": answer,
            "resume_context": resume_context,
            "job_description": job_description,
            "interview_history": interview_history,
        }
    )

    # ========================================================
    # Safety check
    # ========================================================

    if isinstance(result, InterviewEvaluationResult):
        return result

    if isinstance(result, dict):
        return InterviewEvaluationResult.model_validate(result)

    raise TypeError(
        f"Unexpected evaluation result type: "
        f"{type(result).__name__}"
    )