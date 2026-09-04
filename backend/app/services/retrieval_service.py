from app.rag.vector_store import get_retriever


def retrieve_resume(
    query: str,
    k: int = 5,
) -> list[str]:
    """
    Retrieve relevant information from the candidate's resume.
    """

    if not query.strip():
        return []

    retriever = get_retriever(
        document_type="resume",
        k=k,
    )

    documents = retriever.invoke(query)

    return [
        document.page_content
        for document in documents
    ]


def retrieve_job_description(
    query: str,
    k: int = 5,
) -> list[str]:
    """
    Retrieve relevant information from the job description.
    """

    if not query.strip():
        return []

    retriever = get_retriever(
        document_type="job_description",
        k=k,
    )

    documents = retriever.invoke(query)

    return [
        document.page_content
        for document in documents
    ]