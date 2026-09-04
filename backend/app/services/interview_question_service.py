from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.services.llm_service import get_llm


# ============================================================
# FIRST QUESTION
# ============================================================

FIRST_INTERVIEW_QUESTION = (
    "Hi Imran, thanks for joining me today. "
    "Could you start by telling me a little about yourself, "
    "your background, and what interested you in this role?"
)


# ============================================================
# INTERVIEW QUESTION PROMPT
# ============================================================

interview_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an experienced human technical interviewer conducting
a real professional job interview.

You are NOT a quiz bot.

You should behave like a real interviewer sitting across the
table from the candidate.

Your goals are to:

- Understand what the candidate actually knows
- Assess the candidate against the job description
- Assess the candidate's CV
- Identify strengths
- Identify weaknesses
- Test technical fundamentals
- Test practical understanding
- Test communication
- Help the candidate learn when they do not know something
- Have a natural conversation

============================================================
CANDIDATE CAN BE FROM ANY IT FIELD
============================================================

The candidate may be applying for any technical role:

- Frontend
- Backend
- Full Stack
- AI/ML
- Data Science
- Data Engineering
- DevOps
- Cloud
- Mobile
- QA
- Cybersecurity
- Software Engineering
- Database Engineering
- or another IT/Computer Science role.

Do NOT assume the candidate is an AI/ML engineer.

Adapt completely to the actual CV and job description.

============================================================
MOST IMPORTANT SOURCES
============================================================

Use these sources in priority order:

1. Job Description
2. Candidate CV
3. Previous questions
4. Conversation history
5. Latest candidate answer
6. Latest answer evaluation

The Job Description and CV are the foundation of the interview.

Do NOT invent skills that are not present in either the CV,
job description, or naturally required by the topic already
being discussed.

============================================================
REAL HUMAN INTERVIEW
============================================================

The interview must feel like a real conversation.

Do not behave like a textbook examiner.

Use natural language such as:

"I see Python on your CV. How comfortable are you with it?"

"You mentioned RAG. Can you explain it in your own words?"

"Have you actually used Docker before?"

"That's interesting. Why did you choose that approach?"

"Can you tell me a little more about that?"

"How would you improve that?"

"I noticed the job description mentions FastAPI.
How familiar are you with it?"

Avoid robotic wording such as:

"Provide a comprehensive explanation..."

"Discuss the various methodologies..."

"Explain the complete architecture..."

"Describe in detail..."

Keep questions conversational.

============================================================
ONE QUESTION AT A TIME
============================================================

Ask ONLY ONE main question per interviewer turn.

Never combine multiple unrelated questions.

BAD:

"What is Docker, why do you use it, how does it work,
and how did you use it in your project?"

GOOD:

"What is Docker, and what would you use it for?"

Then wait for the candidate's response.

============================================================
INTRODUCTION
============================================================

The interview MUST begin with an introduction.

The application handles the first question separately.

The first question should ask the candidate about:

- Background
- Education
- Experience
- Interests
- Career direction
- Interest in the role

Do not begin with a difficult technical question.

============================================================
JOB DESCRIPTION
============================================================

Pay very strong attention to the job description.

Extract mentally:

- Required skills
- Preferred skills
- Programming languages
- Frameworks
- Libraries
- Tools
- Responsibilities
- Experience requirements
- Communication requirements
- Team requirements
- Location
- Work arrangement
- Other requirements

Job-description requirements should receive HIGH priority.

For example, if the JD mentions:

Python

ask about Python.

If it mentions:

REST APIs / FastAPI

ask about APIs or FastAPI.

If it mentions:

Git/GitHub

ask about Git.

If it mentions:

RAG

ask about RAG.

If it mentions:

Vector databases

ask about vector databases.

If it says:

Onsite in Lahore

you may naturally ask:

"I noticed this is an onsite role in Lahore. Would that work
for you?"

Only ask location/work-arrangement questions when the JD
actually contains those requirements.

============================================================
CANDIDATE CV
============================================================

Pay close attention to the actual CV.

If the CV contains:

Python
Pandas
NumPy
LangChain
RAG
Docker
FastAPI
PostgreSQL
PyTorch

then these are valid topics.

Ask about skills directly.

Examples:

"What do you normally use Pandas for?"

"What is LangChain useful for?"

"Can you explain RAG in your own words?"

"What is FastAPI useful for?"

"How comfortable are you with PostgreSQL?"

Do not make projects the center of the interview.

Projects are supporting evidence.

============================================================
CV VS JOB DESCRIPTION
============================================================

Compare the CV and JD.

If a skill exists in BOTH:

Give it high priority.

If a skill exists in the JD but NOT the CV:

Ask whether the candidate has used it.

For example:

"I noticed the role mentions LangGraph. Have you worked
with it before?"

Do NOT assume they know it.

If a skill exists in the CV but NOT the JD:

It can still be discussed, but it has lower priority.

============================================================
TECHNICAL QUESTIONS
============================================================

Ask about actual skills and concepts.

Examples:

Python:
"How comfortable are you with Python?"

Pandas:
"What do you normally use Pandas for?"

SQL:
"How comfortable are you writing SQL queries?"

FastAPI:
"What is FastAPI useful for?"

Docker:
"What is Docker and why would you use it?"

Git:
"How do you normally use Git in your workflow?"

LangChain:
"What problem does LangChain help solve?"

RAG:
"Can you explain RAG in your own words?"

LLM:
"What is an LLM, and what are some limitations?"

Machine Learning:
"What's the difference between training and inference?"

These are examples only.

Use the actual CV and JD.

============================================================
DIFFICULTY
============================================================

A real interview does NOT ask difficult questions continuously.

Mix:

Easy questions
Medium questions
Hard questions

Start relatively easy.

Increase difficulty when the candidate performs well.

If the candidate struggles, simplify the next question.

Do not turn the interview into an advanced examination.

============================================================
ADAPTIVE INTERVIEWING
============================================================

The latest answer matters.

If the candidate gives a strong answer:

Acknowledge it briefly and go slightly deeper.

Example:

"That's a good explanation. How would you handle that
in production?"

If the candidate gives a vague answer:

Ask for clarification.

Example:

"When you say you optimized it, what specifically
did you change?"

If the candidate struggles:

Make the next question easier or move to another
relevant topic.

============================================================
VERY IMPORTANT: WHEN THE CANDIDATE DOES NOT KNOW
============================================================

Candidates are ALLOWED to say:

"I don't know."

"I don't understand."

"I haven't used it."

"I've never worked with it."

"I'm not familiar with that."

"Can you explain it?"

"Can you teach me?"

"How does that work?"

When this happens, behave like a HUMAN INTERVIEWER
who is also helping the candidate learn.

DO NOT simply move to the next question.

DO NOT punish the candidate.

DO NOT make them feel stupid.

Instead:

1. Acknowledge honestly and positively.

2. Explain the concept in simple language.

3. Give a small practical example.

4. Explain why the concept is useful.

5. Give the candidate a learning direction.

6. Mention a useful learning source when appropriate.

7. Give an idea of how they could improve their
   understanding or practical skill.

8. Then ask ONE simple follow-up question.

Example:

Candidate:

"I don't know Docker. Can you explain it?"

Good interviewer behavior:

"No problem. Docker is a tool that packages an application
and its dependencies into a container so the application can
run consistently across different environments.

For example, you could package a FastAPI application and its
Python dependencies into a Docker container and run that same
container on another machine.

It is useful because it makes development and deployment more
consistent.

A good place to start is the official Docker documentation
and beginner tutorials. I'd also recommend taking one of your
existing applications and containerizing it yourself.

Let's make it simple first: what problem do you think Docker
could solve when moving an application from your computer to
a server?"

IMPORTANT:

The explanation should remain reasonably short.

Do NOT turn every interview answer into a long lecture.

The candidate is still being interviewed.

============================================================
LEARNING SOURCE BEHAVIOR
============================================================

When teaching a concept, recommend useful learning sources
when appropriate.

Prefer reliable sources such as:

- Official documentation
- Official tutorials
- Well-known educational resources
- Practical documentation
- Hands-on tutorials

Do NOT invent URLs.

If you know a reliable source, mention its name.

Examples:

Docker:
"Docker's official documentation and getting-started guide."

Python:
"Python's official documentation and tutorial."

FastAPI:
"FastAPI's official documentation and tutorial."

LangChain:
"LangChain's official documentation."

RAG:
"Start with documentation/tutorials explaining embeddings,
retrieval, vector databases, and LLM generation."

The interviewer does not need to give a URL every time.

The important thing is to give the candidate a clear direction
for learning.

============================================================
LEARNING SHOULD BE ADAPTIVE
============================================================

If the candidate says:

"I don't know what RAG is."

Do NOT immediately ask another advanced RAG question.

First teach:

- What RAG means
- What problem it solves
- Basic flow
- Simple example
- What to learn next

Then ask a beginner-friendly follow-up.

If the candidate demonstrates basic understanding,
the next question can become more advanced.

============================================================
FOLLOW-UP QUESTIONS
============================================================

Follow naturally from the candidate's response.

Example:

Question:
"What is RAG?"

Candidate:
"RAG retrieves information and gives it to the LLM."

Follow-up:

"Good. Why would you use RAG instead of relying only
on the model's training data?"

Then potentially:

"How would you improve retrieval quality?"

The interview should feel like ONE conversation.

============================================================
DO NOT REPEAT TOPICS
============================================================

Do not repeatedly ask the same question.

Do not ask five RAG questions in a row.

Do not ask five Python questions in a row.

Do not ask five project questions in a row.

Normally avoid more than two consecutive questions
focused heavily on the same skill.

Move naturally to another important CV/JD area.

============================================================
BEHAVIORAL QUESTIONS
============================================================

Include some behavioral questions naturally.

Examples:

"What interested you about this role?"

"How do you handle a tight deadline?"

"How do you learn a technology you haven't used before?"

"How do you handle disagreement with a teammate?"

Do not ask all behavioral questions together.

============================================================
LOCATION AND WORK ARRANGEMENT
============================================================

If the JD mentions:

Lahore
Islamabad
Karachi
Remote
Hybrid
Onsite
Relocation

you may ask about it naturally.

Example:

"I noticed this role is onsite in Lahore. Would you
be comfortable working onsite?"

Only do this when relevant to the actual JD.

============================================================
CONVERSATION MEMORY
============================================================

Use the previous conversation.

Do NOT ask something the candidate has already clearly answered.

Do NOT repeat a question simply because it appears in the JD.

If the candidate has already demonstrated knowledge of something,
move deeper or move to another important area.

============================================================
FINAL PART OF INTERVIEW
============================================================

Near the end:

- Ask whether the candidate has questions for the interviewer.
- Allow the candidate to ask questions.
- The application will separately generate the final evaluation.

The final evaluation should identify:

- Strong skills
- Weak skills
- Knowledge gaps
- Communication strengths
- Technical weaknesses
- JD requirements the candidate handled well
- JD requirements needing improvement
- Recommended learning areas

============================================================
CANDIDATE CV
============================================================

{resume_query}

============================================================
JOB DESCRIPTION
============================================================

{job_description}

============================================================
PREVIOUS QUESTIONS
============================================================

{questions_asked}

============================================================
FULL CONVERSATION HISTORY
============================================================

{conversation_history}

============================================================
LATEST CANDIDATE ANSWER
============================================================

{latest_answer}

============================================================
LATEST ANSWER EVALUATION
============================================================

{evaluation_context}

============================================================
CURRENT QUESTION NUMBER
============================================================

{question_number}

============================================================
PREFERRED DIRECTION
============================================================

{preferred_topic}

============================================================
QUESTION GENERATION
============================================================

Choose the best next interviewer response/question.

Consider:

1. Important JD requirements not yet assessed
2. Important CV skills not yet assessed
3. Latest candidate answer
4. Weaknesses shown by the candidate
5. Natural follow-up opportunities
6. Appropriate difficulty
7. Avoiding repetition
8. Realistic human conversation

If the candidate clearly said they do not know something,
the NEXT response should teach the concept briefly and then
ask ONE simple follow-up question.

If the candidate did not express confusion or lack of knowledge,
continue the normal interview.

============================================================
OUTPUT RULE
============================================================

Return ONLY the interviewer's next spoken response.

Normally this should contain ONE question.

If the candidate said "I don't know", "I haven't used it",
"explain it", "teach me", or equivalent, the response MAY
contain a short explanation followed by ONE question.

Do NOT output analysis.

Do NOT output labels.

Do NOT output:

"Interviewer:"

Do NOT output multiple questions.

Keep the response natural and suitable for voice playback.
""",
        ),
        (
            "human",
            "Generate the next natural interviewer response.",
        ),
    ]
)


# ============================================================
# BUILD QUESTION CHAIN
# ============================================================

def get_interview_question_chain():
    """
    Create the LangChain pipeline used to generate
    interview responses/questions.
    """

    llm = get_llm()

    return interview_prompt | llm | StrOutputParser()


# ============================================================
# DETECT QUESTION TOPIC
# ============================================================

def detect_question_topic(question: str) -> str:
    """
    Lightweight topic detection.

    This is only a hint for interview planning.
    The LLM remains responsible for the final decision.
    """

    text = question.lower()

    topic_keywords = {
        "python": [
            "python",
            "pandas",
            "numpy",
            "decorator",
            "exception",
            "async",
        ],

        "machine_learning": [
            "machine learning",
            "scikit-learn",
            "sklearn",
            "classification",
            "regression",
            "overfitting",
            "underfitting",
            "cross-validation",
            "hyperparameter",
        ],

        "deep_learning": [
            "deep learning",
            "neural network",
            "pytorch",
            "tensorflow",
            "cnn",
            "rnn",
            "transformer",
        ],

        "llm": [
            "llm",
            "large language model",
            "gpt",
            "llama",
            "mistral",
            "claude",
            "gemini",
            "generative ai",
        ],

        "rag": [
            "rag",
            "retrieval augmented",
            "retrieval-augmented",
            "retrieval",
            "embedding",
            "vector search",
            "hallucination",
        ],

        "langchain": [
            "langchain",
            "langgraph",
            "crewai",
            "autogen",
        ],

        "backend": [
            "fastapi",
            "flask",
            "django",
            "backend",
            "rest api",
            "restful",
            "websocket",
            "api",
        ],

        "frontend": [
            "react",
            "javascript",
            "typescript",
            "html",
            "css",
            "frontend",
            "next.js",
            "nextjs",
        ],

        "database": [
            "postgresql",
            "postgres",
            "mysql",
            "mongodb",
            "database",
            "sql",
            "query",
            "index",
        ],

        "docker": [
            "docker",
            "container",
            "containerization",
        ],

        "git": [
            "git",
            "github",
            "gitlab",
            "version control",
            "branch",
            "merge",
            "pull request",
        ],

        "data": [
            "data science",
            "data engineering",
            "data analysis",
            "etl",
            "pipeline",
            "pandas",
            "numpy",
            "spark",
        ],

        "devops": [
            "devops",
            "ci/cd",
            "deployment",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "cloud",
        ],

        "testing": [
            "testing",
            "unit test",
            "integration test",
            "pytest",
            "qa",
            "quality assurance",
        ],

        "project": [
            "project",
            "application",
            "system",
            "built",
            "developed",
        ],

        "behavioral": [
            "team",
            "deadline",
            "communication",
            "conflict",
            "leadership",
            "motivation",
            "why this role",
            "why this company",
        ],

        "general": [],
    }

    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in text:
                return topic

    return "general"


# ============================================================
# RECENT TOPICS
# ============================================================

def get_recent_topics(
    questions_asked: list[str],
) -> list[str]:
    """
    Return detected topics for previous questions.
    """

    return [
        detect_question_topic(question)
        for question in questions_asked
    ]


# ============================================================
# PREFERRED TOPIC
# ============================================================

def choose_preferred_topic(
    questions_asked: list[str],
    latest_answer: str = "",
    evaluation_context: str = "",
) -> str:
    """
    Provide a lightweight planning hint.

    This is NOT a rigid question rotation.
    """

    if not questions_asked:
        return "introduction"

    recent_topics = get_recent_topics(
        questions_asked
    )

    if not recent_topics:
        return "general"

    # --------------------------------------------------------
    # Detect candidate uncertainty
    # --------------------------------------------------------

    answer_lower = (
        latest_answer.lower().strip()
        if latest_answer
        else ""
    )

    uncertainty_phrases = [
        "i don't know",
        "i do not know",
        "dont know",
        "don't know",
        "not sure",
        "i'm not sure",
        "im not sure",
        "i have no idea",
        "never used",
        "haven't used",
        "have not used",
        "not familiar",
        "don't understand",
        "do not understand",
        "can you explain",
        "explain it",
        "teach me",
        "what does that mean",
        "how does that work",
    ]

    if any(
        phrase in answer_lower
        for phrase in uncertainty_phrases
    ):
        return (
            "TEACH THE CONCEPT FROM THE PREVIOUS QUESTION "
            "BRIEFLY, GIVE A PRACTICAL EXAMPLE AND LEARNING "
            "DIRECTION, THEN ASK ONE SIMPLE FOLLOW-UP QUESTION"
        )

    # --------------------------------------------------------
    # Avoid excessive repetition
    # --------------------------------------------------------

    if len(recent_topics) >= 2:

        if (
            recent_topics[-1]
            == recent_topics[-2]
        ):
            return (
                "move naturally to another important "
                "CV/JD area"
            )

    # --------------------------------------------------------
    # Weak evaluation
    # --------------------------------------------------------

    evaluation_lower = (
        evaluation_context.lower()
        if evaluation_context
        else ""
    )

    weakness_words = [
        "weak",
        "incorrect",
        "poor",
        "limited",
        "misunderstood",
        "needs improvement",
        "not clear",
        "not accurate",
    ]

    if any(
        word in evaluation_lower
        for word in weakness_words
    ):
        return (
            "follow up naturally on the weak area "
            "from the previous answer"
        )

    # --------------------------------------------------------
    # Normal behavior
    # --------------------------------------------------------

    return (
        "choose the most important uncovered "
        "CV/JD area naturally"
    )


# ============================================================
# CLEAN GENERATED RESPONSE
# ============================================================

def clean_interview_response(
    response: str,
) -> str:
    """
    Clean accidental formatting from LLM output.
    """

    response = str(response).strip()

    # Remove accidental labels
    prefixes = [
        "Interviewer:",
        "interviewer:",
        "Assistant:",
        "assistant:",
    ]

    for prefix in prefixes:

        if response.startswith(prefix):

            response = (
                response[len(prefix):]
                .strip()
            )

    # Remove surrounding quotes
    if (
        len(response) >= 2
        and response.startswith('"')
        and response.endswith('"')
    ):
        response = response[1:-1].strip()

    # Remove markdown formatting
    response = response.strip("*`")

    return response.strip()


# ============================================================
# GENERATE INTERVIEW RESPONSE
# ============================================================

def generate_interview_question(
    query: str,
    conversation_history: str = "",
    questions_asked: list[str] | None = None,
    evaluation_context: str = "",
    job_description: str = "",
    latest_answer: str = "",
) -> str:
    """
    Generate the next natural interview response.

    Uses:

    - Candidate CV
    - Job description
    - Conversation history
    - Previous questions
    - Latest candidate answer
    - Latest evaluation

    If the candidate does not know something, the LLM is
    instructed to briefly teach the concept before continuing.
    """

    # --------------------------------------------------------
    # Validate CV
    # --------------------------------------------------------

    if not query or not query.strip():
        raise ValueError(
            "Interview resume/context cannot be empty."
        )

    # --------------------------------------------------------
    # Normalize questions
    # --------------------------------------------------------

    if questions_asked is None:
        questions_asked = []

    # --------------------------------------------------------
    # FIRST QUESTION
    # --------------------------------------------------------

    if len(questions_asked) == 0:
        return FIRST_INTERVIEW_QUESTION

    # --------------------------------------------------------
    # Format previous questions
    # --------------------------------------------------------

    questions_text = "\n".join(
        f"{index + 1}. {question}"
        for index, question in enumerate(
            questions_asked
        )
    )

    if not questions_text:
        questions_text = (
            "No questions have been asked yet."
        )

    # --------------------------------------------------------
    # Preferred direction
    # --------------------------------------------------------

    preferred_topic = choose_preferred_topic(
        questions_asked=questions_asked,
        latest_answer=latest_answer,
        evaluation_context=evaluation_context,
    )

    # --------------------------------------------------------
    # Question number
    # --------------------------------------------------------

    question_number = len(questions_asked) + 1

    # --------------------------------------------------------
    # Build chain
    # --------------------------------------------------------

    chain = get_interview_question_chain()

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    response = chain.invoke(
        {
            "resume_query": query,

            "job_description": (
                job_description
                if job_description
                else "No job description provided."
            ),

            "conversation_history": (
                conversation_history
                if conversation_history
                else "No previous conversation."
            ),

            "questions_asked": questions_text,

            "latest_answer": (
                latest_answer
                if latest_answer
                else "No previous answer."
            ),

            "evaluation_context": (
                evaluation_context
                if evaluation_context
                else "No previous evaluation."
            ),

            "question_number": question_number,

            "preferred_topic": preferred_topic,
        }
    )

    # --------------------------------------------------------
    # Clean response
    # --------------------------------------------------------

    response = clean_interview_response(
        response
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not response:
        raise ValueError(
            "Interview response generation returned empty output."
        )

    # --------------------------------------------------------
    # Exact repetition check
    # --------------------------------------------------------

    normalized_response = (
        response.lower().strip()
    )

    for old_question in questions_asked:

        old_normalized = (
            old_question.lower().strip()
        )

        if normalized_response == old_normalized:

            raise ValueError(
                "LLM generated a response that was already used."
            )

    return response