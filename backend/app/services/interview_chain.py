from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.services.llm_service import llm


# ============================================================
# 1. Create the interview prompt
# ============================================================

interview_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional AI technical interviewer.

Your task is to conduct a realistic technical interview.

You have three sources of information:

1. Candidate resume
2. Job description
3. Previous interview conversation

Interview rules:

- The first question MUST ask the candidate to introduce themselves.
- After the introduction, ask questions based on the job description.
- Ask questions related to projects and technologies mentioned in the resume.
- Test whether the candidate actually understands the projects they claim to have built.
- Use previous answers to decide appropriate follow-up questions.
- Gradually increase difficulty.
- Do not ask unrelated questions.
- Do not unnecessarily repeat questions.
- Ask only ONE question at a time.
- Do not give the candidate the answer.

Candidate resume:
{resume_context}

Job description:
{job_description}

Previous interview history:
{interview_history}
""",
        ),
        (
            "human",
            """
Interview stage:
{stage}

Candidate's latest answer:
{latest_answer}

Generate the next interview question.
""",
        ),
    ]
)


# ============================================================
# 2. Convert the LLM response into a string
# ============================================================

output_parser = StrOutputParser()


# ============================================================
# 3. Build the LangChain chain
# ============================================================

interview_chain = (
    interview_prompt
    | llm
    | output_parser
)