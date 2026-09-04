from langchain_chroma import Chroma

from app.core.config import settings
from app.rag.embeddings import embeddings


# ============================================================
# 1. Create LangChain Chroma Vector Store
# ============================================================

vector_store = Chroma(
    collection_name="interview_documents",
    embedding_function=embeddings,
    persist_directory=settings.chroma_db_path,
)


# ============================================================
# 2. Create a LangChain Retriever
# ============================================================

def get_retriever(
    document_type: str | None = None,
    k: int = 5,
):
    """
    Create a LangChain retriever for interview documents.

    document_type:
        None              -> search all documents
        "resume"          -> search only resume chunks
        "job_description" -> search only job-description chunks

    k:
        Number of relevant chunks to retrieve.
    """

    search_kwargs = {
        "k": k,
    }

    # --------------------------------------------------------
    # Optional metadata filter
    # --------------------------------------------------------

    if document_type:
        search_kwargs["filter"] = {
            "document_type": document_type,
        }

    # --------------------------------------------------------
    # Convert Chroma vector store into LangChain retriever
    # --------------------------------------------------------

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs,
    )