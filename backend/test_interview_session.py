from app.services.interview_service import InterviewSession


def main():

    # ========================================================
    # Create Interview Session
    # ========================================================

    session = InterviewSession(
        resume_query="""
        AI/ML Engineer
        Software Developer
        LLM and Generative AI Specialist

        Experience:
        Funsol Technologies
        Mentimotive
        Multimodal AI
        DistilBERT
        Wav2Vec 2.0
        Whisper
        FastAPI
        LangChain
        ChromaDB
        JWT
        Docker

        Genesys Research Lab
        AI Fitness Coach
        MediaPipe
        OpenCV
        DTW
        WebSockets
        PostgreSQL

        Projects:
        AI Medical Chatbot
        RAG
        HuggingFace
        FAISS
        Mistral-7B

        Autonomous Dental Appointment Voice Agent
        VAPI
        Make.com

        Secure Task Manager
        FastAPI
        PostgreSQL

        Skills:
        Python
        Machine Learning
        Deep Learning
        LLMs
        RAG
        Agentic AI
        LangChain
        FastAPI
        Docker
        Git
        GitHub
        SQL
        PostgreSQL
        PyTorch
        TensorFlow
        HuggingFace
        FAISS
        ChromaDB
        """,

        job_description="""
        AI/ML Engineer

        Responsibilities:
        Build and deploy machine learning and AI applications.
        Develop backend APIs for AI systems.
        Work with Large Language Models and Generative AI.
        Build Retrieval-Augmented Generation systems.
        Integrate AI models into production applications.
        Work with databases and APIs.
        Write clean and maintainable Python code.
        Collaborate using Git and GitHub.

        Requirements:
        Python
        Machine Learning
        Deep Learning
        TensorFlow or PyTorch
        Large Language Models
        Generative AI
        RAG
        LangChain
        FastAPI
        Docker
        Git
        GitHub
        SQL
        PostgreSQL
        API development
        Problem solving
        """
    )

    # ========================================================
    # Interview Loop
    # ========================================================

    number_of_questions = 10

    for question_number in range(1, number_of_questions + 1):

        print("\n" + "=" * 50)
        print(f"QUESTION {question_number}")
        print("=" * 50)

        # Generate next question
        question = session.get_next_question()

        print(question)

        # Get candidate answer
        answer = input("\nCandidate Answer: ")

        # Save and evaluate answer
        session.add_candidate_answer(answer)

    # ========================================================
    # Complete Interview History
    # ========================================================

    print("\n" + "=" * 50)
    print("INTERVIEW HISTORY")
    print("=" * 50)

    print(session.get_history())

    # ========================================================
    # Final Interview Report
    # ========================================================

    print("\n" + "=" * 50)
    print("FINAL INTERVIEW REPORT")
    print("=" * 50)

    report = session.generate_final_report()

    # ========================================================
    # Overall Score
    # ========================================================

    print("\nOverall Score:", report.overall_score)

    # ========================================================
    # Technical Performance
    # ========================================================

    print("\nTechnical Performance:")
    print(report.technical_performance)

    # ========================================================
    # Communication
    # ========================================================

    print("\nCommunication:")
    print(report.communication)

    # ========================================================
    # Strengths
    # ========================================================

    print("\nStrengths:")

    for item in report.strengths:
        print("-", item)

    # ========================================================
    # Weaknesses
    # ========================================================

    print("\nWeaknesses:")

    for item in report.weaknesses:
        print("-", item)

    # ========================================================
    # Skills Demonstrated
    # ========================================================

    print("\nSkills Demonstrated:")

    for item in report.skills_demonstrated:
        print("-", item)

    # ========================================================
    # Skills To Improve
    # ========================================================

    print("\nSkills To Improve:")

    for item in report.skills_to_improve:
        print("-", item)

    # ========================================================
    # Job Fit
    # ========================================================

    print("\nJob Fit:")
    print(report.job_fit)

    # ========================================================
    # Recommendations
    # ========================================================

    print("\nRecommendations:")

    for item in report.recommendations:
        print("-", item)


if __name__ == "__main__":
    main()