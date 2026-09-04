from app.services.retrieval_service import (
    retrieve_resume,
    retrieve_job_description,
)


def extract_documents(results) -> list[str]:
    """
    Extract document text from ChromaDB results.
    """

    if not results:
        return []

    documents = results.get("documents")

    if not documents:
        return []

    return documents[0]


def build_interview_context(
    query: str,
    n_results: int = 5,
) -> dict:
    """
    Retrieve relevant resume and job-description
    information and combine them into interview context.
    """

    resume_results = retrieve_resume(
        query=query,
        n_results=n_results,
    )

    job_results = retrieve_job_description(
        query=query,
        n_results=n_results,
    )

    resume_chunks = extract_documents(
        resume_results
    )

    job_chunks = extract_documents(
        job_results
    )

    return {
        "resume_context": "\n\n".join(resume_chunks),
        "job_description_context": "\n\n".join(job_chunks),
    }