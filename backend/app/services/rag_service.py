from app.rag.embeddings import generate_embeddings
from app.rag.vector_store import search_documents


def retrieve_relevant_documents(
    query: str,
    top_k: int = 3,
) -> list[str]:

    query_embedding = generate_embeddings([query])[0]

    results = search_documents(
        query_embedding=query_embedding,
        n_results=top_k,
    )

    documents = results.get("documents", [])

    if not documents:
        return []

    return documents[0]