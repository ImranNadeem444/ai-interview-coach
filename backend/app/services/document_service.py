from pathlib import Path

from langchain_core.documents import Document

from app.rag.loaders import (
    load_pdf,
    load_docx,
    load_txt,
)

from app.rag.chunker import chunk_text

from app.rag.vector_store import vector_store


def load_document(file_path: str) -> str:
    """
    Load a document and extract its text.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".docx":
        return load_docx(file_path)

    if extension == ".txt":
        return load_txt(file_path)

    raise ValueError("Unsupported file type")


def ingest_document(
    file_path: str,
    document_type: str,
):
    """
    Process an uploaded document using LangChain.

    File
      ↓
    Extract text
      ↓
    Create chunks
      ↓
    Convert chunks to LangChain Documents
      ↓
    LangChain Chroma
      ↓
    Embeddings + storage
    """

    # =========================================================
    # 1. Extract text
    # =========================================================

    text = load_document(file_path)

    if not text.strip():
        raise ValueError(
            "Document contains no readable text"
        )

    # =========================================================
    # 2. Create chunks
    # =========================================================

    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            "Document produced no chunks"
        )

    # =========================================================
    # 3. Get file name
    # =========================================================

    file_name = Path(file_path).name

    # =========================================================
    # 4. Convert chunks into LangChain Documents
    # =========================================================

    documents = []

    for chunk in chunks:

        # Our chunker returns dictionaries.
        if isinstance(chunk, dict):

            chunk_text_value = chunk.get(
                "text",
                ""
            )

            section = chunk.get(
                "section",
                ""
            )

        else:

            chunk_text_value = chunk
            section = ""

        # Ignore empty chunks
        if not chunk_text_value:
            continue

        if not chunk_text_value.strip():
            continue

        # Create LangChain Document
        document = Document(
            page_content=chunk_text_value,
            metadata={
                "document_type": document_type,
                "file_name": file_name,
                "section": section or "unknown",
            },
        )

        documents.append(document)

    # =========================================================
    # 5. Make sure we actually created Documents
    # =========================================================

    if not documents:
        raise ValueError(
            "No valid text found in document chunks"
        )

    # =========================================================
    # 6. Create unique IDs
    # =========================================================

    ids = [
        f"{document_type}_{file_name}_{i}"
        for i in range(len(documents))
    ]

    # =========================================================
    # 7. Store using LangChain Chroma
    # =========================================================

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    # =========================================================
    # 8. Return result
    # =========================================================

    return {
        "file_name": file_name,
        "document_type": document_type,
        "chunks_created": len(documents),
    }


def ingest_text(
    text: str,
    document_type: str,
):
    """
    Process pasted text using LangChain.
    """

    # =========================================================
    # 1. Validate text
    # =========================================================

    if not text.strip():
        raise ValueError(
            "Text contains no readable content"
        )

    # =========================================================
    # 2. Create chunks
    # =========================================================

    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            "Text produced no chunks"
        )

    # =========================================================
    # 3. Convert chunks into LangChain Documents
    # =========================================================

    documents = []

    for chunk in chunks:

        if isinstance(chunk, dict):

            chunk_text_value = chunk.get(
                "text",
                ""
            )

            section = chunk.get(
                "section",
                ""
            )

        else:

            chunk_text_value = chunk
            section = ""

        if not chunk_text_value:
            continue

        if not chunk_text_value.strip():
            continue

        document = Document(
            page_content=chunk_text_value,
            metadata={
                "document_type": document_type,
                "source": "pasted_text",
                "section": section or "unknown",
            },
        )

        documents.append(document)

    # =========================================================
    # 4. Validate Documents
    # =========================================================

    if not documents:
        raise ValueError(
            "No valid text found in chunks"
        )

    # =========================================================
    # 5. Create unique IDs
    # =========================================================

    ids = [
        f"{document_type}_pasted_{i}"
        for i in range(len(documents))
    ]

    # =========================================================
    # 6. Store using LangChain Chroma
    # =========================================================

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    # =========================================================
    # 7. Return result
    # =========================================================

    return {
        "document_type": document_type,
        "chunks_created": len(documents),
    }