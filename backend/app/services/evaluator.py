from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_service import llm


# ============================================================
# EVALUATION RESULT
# ============================================================

class InterviewEvaluationResult(BaseModel):
    score: int = Field(
        ge=0,
        le=10,
    )

    technical_accuracy: str

    relevance: str

    strengths: List[str]

    weaknesses: List[str]

    improvement: str

    follow_up_needed: bool


# ============================================================
# EVALUATION PROMPT
# ============================================================

evaluation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert technical interview evaluator.

Evaluate the candidate's answer to the interview question.

Consider:

1. Technical correctness
2. Understanding of the concept
3. Relevance to the question
4. Depth of explanation
5. Practical experience
6. Communication clarity

Give a score from 0 to 10.

Scoring guidance:

0-2:
Very poor or completely incorrect.

3-4:
Weak understanding.

5-6:
Basic understanding but significant gaps.

7-8:
Good understanding with minor gaps.

9:
Very strong answer.

10:
Excellent expert-level answer.

Do not punish a candidate simply because the answer is short
if the answer is technically correct.

Identify:

- Technical accuracy
- Relevance
- Strengths
- Weaknesses
- How the candidate can improve
- Whether a follow-up question is useful

Return structured data.
""",
        ),
        (
            "human",
            """
Interview Question:

{question}

Candidate Answer:

{answer}
""",
        ),
    ]
)


# ============================================================
# STRUCTURED EVALUATION CHAIN
# ============================================================

evaluation_chain = evaluation_prompt | llm.with_structured_output(
    InterviewEvaluationResult
)


# ============================================================
# EVALUATE ANSWER
# ============================================================

def evaluate_interview_answer(
    question: str,
    answer: str,
) -> InterviewEvaluationResult:
    """
    Evaluate one candidate answer.
    """

    if not question.strip():
        raise ValueError(
            "Interview question cannot be empty."
        )

    if not answer.strip():
        raise ValueError(
            "Candidate answer cannot be empty."
        )

    result = evaluation_chain.invoke(
        {
            "question": question,
            "answer": answer,
        }
    )

    return result