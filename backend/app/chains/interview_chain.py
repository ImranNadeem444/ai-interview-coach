from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.services.llm_service import llm


# ============================================================
# INTERVIEW QUESTION PROMPT
# ============================================================

interview_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional AI technical interviewer.

Your job is to conduct a realistic, adaptive technical interview.

You have access to:

1. Candidate resume
2. Job description
3. Previous interview conversation
4. Questions already asked
5. Candidate's latest answer
6. Latest evaluation

============================================================
INTERVIEW RULES
============================================================

The first question MUST ask the candidate to introduce
themselves.

After the introduction:

- Ask questions relevant to the job description.
- Ask questions about technologies in the resume.
- Ask about projects mentioned in the resume.
- Test whether the candidate actually understands their work.
- Use previous answers to decide follow-up questions.
- Gradually increase difficulty.
- Ask practical technical questions.
- Ask only ONE question at a time.
- Do not provide the answer.
- Do not unnecessarily repeat questions.

============================================================
ADAPTIVE INTERVIEW
============================================================

If the candidate gives a strong answer:

Increase the difficulty and explore the topic deeper.

If the candidate gives a weak answer:

Ask a simpler follow-up or move to another relevant topic.

Do not make every question difficult.

============================================================
TOPIC COVERAGE
============================================================

Prioritize topics relevant to the job.

Possible areas include:

- Python
- Machine Learning
- Deep Learning
- LLMs
- Generative AI
- RAG
- Embeddings
- FAISS
- LangChain
- FastAPI
- PostgreSQL
- SQL
- Docker
- Git
- APIs
- Software Engineering
- Projects from the candidate's resume

Do not force every topic into the interview.

============================================================
QUESTION REPETITION
============================================================

Never repeat a question that has already been asked.

Avoid asking essentially the same question with different wording.

============================================================
CANDIDATE RESUME
============================================================

{resume_context}

============================================================
JOB DESCRIPTION
============================================================

{job_description}

============================================================
PREVIOUS INTERVIEW HISTORY
============================================================

{interview_history}

============================================================
QUESTIONS ALREADY ASKED
============================================================

{questions_asked}

============================================================
LATEST ANSWER
============================================================

{latest_answer}

============================================================
LATEST EVALUATION
============================================================

{evaluation_context}

============================================================
INTERVIEW STAGE
============================================================

{stage}

Generate ONE natural interview question.

Return ONLY the question.

Do not number it.

Do not explain it.

Do not provide an answer.
""",
        ),
        (
            "human",
            "Generate the next interview question.",
        ),
    ]
)


# ============================================================
# OUTPUT PARSER
# ============================================================

output_parser = StrOutputParser()


# ============================================================
# LANGCHAIN CHAIN
# ============================================================

interview_chain = (
    interview_prompt
    | llm
    | output_parser
)


# ============================================================
# GENERATE QUESTION
# ============================================================

def generate_interview_question(
    resume_context: str,
    job_description: str = "",
    interview_history: str = "",
    questions_asked: list[str] | None = None,
    latest_answer: str = "",
    evaluation_context: str = "",
    stage: str = "introduction",
) -> str:
    """
    Generate one interview question.

    Parameters
    ----------
    resume_context:
        Candidate resume or retrieved resume context.

    job_description:
        Job description for the role.

    interview_history:
        Previous questions and candidate answers.

    questions_asked:
        Questions already asked in this interview.

    latest_answer:
        Candidate's most recent answer.

    evaluation_context:
        Evaluation of the latest answer.

    stage:
        Current interview stage.
    """

    if not resume_context.strip():
        raise ValueError(
            "Resume context cannot be empty."
        )

    if questions_asked is None:
        questions_asked = []

    questions_text = "\n".join(
        f"- {question}"
        for question in questions_asked
    )

    response = interview_chain.invoke(
        {
            "resume_context": resume_context,
            "job_description": job_description,
            "interview_history": interview_history,
            "questions_asked": questions_text,
            "latest_answer": latest_answer,
            "evaluation_context": evaluation_context,
            "stage": stage,
        }
    )

    question = response.strip()

    if not question:
        raise ValueError(
            "Interview question generation returned empty output."
        )

    return question