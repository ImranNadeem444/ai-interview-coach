from app.rag.vector_store import get_retriever


def print_documents(title: str, documents):
    """
    Print retrieved LangChain Document objects.
    """

    print("\n" + "=" * 30)
    print(title)
    print("=" * 30)

    for index, document in enumerate(documents, start=1):

        print(f"\n--- Result {index} ---")

        print(document.page_content)

        print("\nMetadata:")
        print(document.metadata)


def main():

    # ========================================================
    # 1. Resume Retriever
    # ========================================================

    resume_retriever = get_retriever(
        document_type="resume",
        k=3,
    )

    resume_documents = resume_retriever.invoke(
        "candidate projects AI applications machine learning"
    )

    print_documents(
        "RESUME SEARCH",
        resume_documents,
    )


    # ========================================================
    # 2. Job Description Retriever
    # ========================================================

    job_retriever = get_retriever(
        document_type="job_description",
        k=3,
    )

    job_documents = job_retriever.invoke(
        "AI Developer Python machine learning LLM RAG LangChain"
    )

    print_documents(
        "JOB DESCRIPTION SEARCH",
        job_documents,
    )


if __name__ == "__main__":
    main()