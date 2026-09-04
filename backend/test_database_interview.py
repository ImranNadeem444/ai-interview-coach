from app.services.interview_service import InterviewSession
from app.db.database import SessionLocal


# ============================================================
# Candidate Resume
# ============================================================

RESUME = """
Imran Nadeem
AI/ML Engineer | Software Developer | LLM & Generative AI Specialist

Education:
BSc Computer Science
NUTECH
Graduated June 2026

Experience:

Funsol Technologies
AI Developer
Oct 2025 - May 2026

Mentimotive:
- Real-time multimodal emotion AI system
- DistilBERT
- Wav2Vec 2.0
- Whisper
- LangChain
- ChromaDB
- FastAPI
- JWT authentication
- Docker

Genesys Research Lab
AI Fitness Coach:
- MediaPipe
- OpenCV
- Dynamic Time Warping (DTW)
- FastAPI
- WebSockets
- PostgreSQL

Projects:

AI Medical Chatbot:
- Retrieval-Augmented Generation (RAG)
- Hugging Face
- FAISS
- Mistral-7B

Autonomous Dental Appointment Voice Agent:
- VAPI
- Make.com

Secure Task Manager:
- FastAPI
- PostgreSQL
- SQL
- Authentication
- API development

Technical Skills:

Programming:
- Python

Machine Learning:
- Machine Learning
- Deep Learning
- Scikit-learn
- TensorFlow
- PyTorch

Generative AI:
- LLMs
- RAG
- Prompt Engineering
- Agentic AI
- Fine-tuning
- Multimodal AI

LLM Technologies:
- GPT
- Gemini
- LLaMA
- Mistral-7B

Frameworks and Libraries:
- LangChain
- ChromaDB
- Hugging Face
- FAISS
- MediaPipe
- OpenCV
- ONNX Runtime

Backend:
- FastAPI
- Django
- Flask
- REST APIs
- WebSockets

Databases:
- PostgreSQL
- MongoDB
- MySQL
- SQL

DevOps and Tools:
- Docker
- Git
- GitHub
- GitHub Actions
- Make.com
- n8n
- VAPI
"""


# ============================================================
# Job Description
# ============================================================

JOB_DESCRIPTION = """
Position: AI/ML Engineer

Responsibilities:

- Build and deploy machine learning and AI applications.
- Develop backend APIs for AI systems.
- Work with Large Language Models and Generative AI.
- Develop Retrieval-Augmented Generation systems.
- Integrate AI models into production applications.
- Work with databases and APIs.
- Write clean and maintainable Python code.
- Develop scalable AI solutions.
- Debug and optimize AI applications.
- Work with other developers and technical teams.
- Use Git and GitHub for software development.

Requirements:

- Python
- Machine Learning
- Deep Learning
- TensorFlow or PyTorch
- Scikit-learn
- Pandas
- Large Language Models
- Generative AI
- RAG
- LangChain
- FastAPI
- REST APIs
- Docker
- Git
- GitHub
- SQL
- PostgreSQL
- API development
- Problem solving
- Software engineering fundamentals

Preferred:

- Experience with embeddings and vector databases.
- Experience with LLM applications.
- Experience with RAG optimization.
- Understanding of hallucination reduction.
- Understanding of model fine-tuning.
- Experience deploying AI applications.
"""


# ============================================================
# Interview Configuration
# ============================================================

TOTAL_QUESTIONS = 10


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("ADAPTIVE DATABASE INTERVIEW TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # Create PostgreSQL database session
    # --------------------------------------------------------

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Create InterviewSession
        # ----------------------------------------------------

        session = InterviewSession(
            db=db,
            resume_query=RESUME,
            job_description=JOB_DESCRIPTION,
        )

        print("\nInterview created successfully.")
        print(f"Interview ID: {session.interview_id}")

        # ----------------------------------------------------
        # Run adaptive interview
        # ----------------------------------------------------

        for question_number in range(
            1,
            TOTAL_QUESTIONS + 1
        ):

            print("\n" + "=" * 60)
            print(f"QUESTION {question_number}")
            print("=" * 60)

            # ------------------------------------------------
            # Generate next question
            # ------------------------------------------------

            question = session.get_next_question()

            print(question)

            # ------------------------------------------------
            # Candidate answer
            # ------------------------------------------------

            answer = input("\nCandidate Answer: ")

            if not answer.strip():

                raise ValueError(
                    "Candidate answer cannot be empty."
                )

            # ------------------------------------------------
            # Save answer and evaluate it
            # ------------------------------------------------

            session.add_candidate_answer(answer)

            # ------------------------------------------------
            # Show evaluation
            # ------------------------------------------------

            print("\n" + "=" * 60)
            print(
                f"QUESTION {question_number} EVALUATION"
            )
            print("=" * 60)

            if session.evaluations:

                print(
                    session.evaluations[-1]
                )

            else:

                print(
                    "No evaluation was generated."
                )

        # ----------------------------------------------------
        # Successful completion
        # ----------------------------------------------------

        print("\n" + "=" * 60)
        print("DATABASE INTERVIEW TEST SUCCESSFUL")
        print("=" * 60)

        print(
            f"Interview ID: "
            f"{session.interview_id}"
        )

        print(
            f"Questions processed: "
            f"{TOTAL_QUESTIONS}"
        )

        print(
            f"Answers processed: "
            f"{TOTAL_QUESTIONS}"
        )

        print(
            f"Evaluations processed: "
            f"{TOTAL_QUESTIONS}"
        )

        print("\nPostgreSQL interview workflow completed.")

    except Exception as exc:

        print("\n" + "=" * 60)
        print("DATABASE INTERVIEW TEST FAILED")
        print("=" * 60)

        print(
            f"Error type: "
            f"{type(exc).__name__}"
        )

        print(
            f"Error message: "
            f"{exc}"
        )

        raise

    finally:

        # ----------------------------------------------------
        # Always close database session
        # ----------------------------------------------------

        db.close()


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()