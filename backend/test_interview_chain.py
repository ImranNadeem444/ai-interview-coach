from app.chains.interview_chain import generate_interview_question


def main():

    # ========================================================
    # Simulate previous interview conversation
    # ========================================================

    conversation_history = """
Interviewer:
Please introduce yourself and tell me about your background,
experience, and what interested you in this role.

Candidate:
I am an AI/ML Engineer with experience in RAG, LangChain,
FastAPI and multimodal AI systems. I built an AI Medical
Chatbot using RAG, FAISS and Mistral-7B.
"""


    # ========================================================
    # Query used for RAG retrieval
    # ========================================================

    query = """
    Candidate experience with RAG, LangChain,
    AI Medical Chatbot, FAISS, Mistral-7B
    """


    # ========================================================
    # Generate next interview question
    # ========================================================

    question = generate_interview_question(
        query=query,
        conversation_history=conversation_history,
    )


    print("=" * 30)
    print("NEXT INTERVIEW QUESTION")
    print("=" * 30)

    print(question)


if __name__ == "__main__":
    main()