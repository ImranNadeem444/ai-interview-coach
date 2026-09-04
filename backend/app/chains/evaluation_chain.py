from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_service import get_llm


# ============================================================
# 1. Evaluation Result Schema
# ============================================================

class InterviewEvaluation(BaseModel):
    """
    Structured result returned by the LLM
    after evaluating a candidate answer.
    """

    score: int = Field(
        ge=1,
        le=10,
        description="Overall answer score from 1 to 10."
    )

    technical_accuracy: str = Field(
        description="Evaluation of the technical correctness."
    )

    relevance: str = Field(
        description="How directly the answer addresses the question."
    )

    strengths: list[str] = Field(
        description="Strong points in the candidate's answer."
    )

    weaknesses: list[str] = Field(
        description="Weak points or missing information."
    )

    improvement: str = Field(
        description="How the candidate can improve the answer."
    )

    follow_up_needed: bool = Field(
        description="Whether the interviewer should ask a follow-up question."
    )


# ============================================================
# 2. Evaluation Prompt
# ============================================================

evaluation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert technical interview evaluator.

Evaluate the candidate's answer realistically, like a human
technical interviewer.

Consider:

1. Technical accuracy
2. Relevance
3. Depth
4. Clarity
5. Communication
6. Concrete examples
7. Whether the candidate actually answered the question

Give an overall score from 1 to 10.

Scoring guidance:

1-3:
Very weak, incorrect, or mostly unrelated answer.

4-5:
Partially correct but missing important information.

6-7:
Good and relevant answer but could use more detail.

8-9:
Strong answer with good technical understanding,
relevant details, and examples.

10:
Excellent answer with strong technical depth,
clear explanation, and strong practical understanding.

Do not penalize the candidate simply because the answer is
short if it is correct and relevant.

Determine whether a follow-up question is needed.

Follow-up should be TRUE when:

- The answer is incorrect.
- The answer is vague.
- Important parts of the question were not answered.
- The candidate claims experience but provides little evidence.
- More detail would reasonably help assess the candidate.

Follow-up should be FALSE when the candidate has already
given a sufficiently strong answer and the interviewer can
naturally move to another topic.

Interview Question:
{question}

Candidate Answer:
{answer}
""",
        ),
        (
            "human",
            "Evaluate the candidate's answer.",
        ),
    ]
)


# ============================================================
# 3. Create Structured Evaluation Chain
# ============================================================

def get_evaluation_chain():

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        InterviewEvaluation
    )

    evaluation_chain = (
        evaluation_prompt
        | structured_llm
    )

    return evaluation_chain


# ============================================================
# 4. Evaluate Answer
# ============================================================

def evaluate_answer(
    question: str,
    answer: str,
) -> InterviewEvaluation:
    """
    Evaluate one candidate answer and return
    a structured InterviewEvaluation object.
    """

    if not question.strip():
        raise ValueError(
            "Interview question cannot be empty."
        )

    if not answer.strip():
        raise ValueError(
            "Candidate answer cannot be empty."
        )

    chain = get_evaluation_chain()

    result = chain.invoke(
        {
            "question": question,
            "answer": answer,
        }
    )

    return result