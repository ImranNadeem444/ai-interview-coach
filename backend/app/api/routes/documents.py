from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)
from pydantic import BaseModel

from app.services.document_service import (
    ingest_document,
    ingest_text,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# JOB DESCRIPTION REQUEST
# ============================================================

class JobDescriptionRequest(BaseModel):
    text: str


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@router.post("/upload/{document_type}")
async def upload_document(
    document_type: str,
    file: UploadFile = File(...),
):
    """
    Upload a resume or job description document.

    Supported:

        POST /documents/upload/resume
        POST /documents/upload/job_description

    Supported file types:

        PDF
        DOCX
        TXT
    """

    print()
    print("=" * 60)
    print("DOCUMENT UPLOAD")
    print("=" * 60)

    print(f"Document type: {document_type}")
    print(f"Filename: {file.filename}")
    print(f"Content type: {file.content_type}")

    # ========================================================
    # 1. Validate document type
    # ========================================================

    allowed_types = {
        "resume",
        "job_description",
    }

    if document_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=(
                "document_type must be "
                "'resume' or 'job_description'"
            ),
        )

    # ========================================================
    # 2. Validate filename
    # ========================================================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename was provided.",
        )

    # ========================================================
    # 3. Validate extension
    # ========================================================

    file_extension = (
        Path(file.filename)
        .suffix
        .lower()
    )

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt",
    }

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF, DOCX and TXT files "
                "are allowed."
            ),
        )

    # ========================================================
    # 4. Create safe filename
    # ========================================================

    original_filename = Path(
        file.filename
    ).name

    file_path = UPLOAD_DIR / original_filename

    # ========================================================
    # 5. Save uploaded file
    # ========================================================

    try:

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

    except Exception as exc:

        print(
            f"UPLOAD SAVE ERROR: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not save uploaded file: {exc}"
            ),
        )

    print(
        f"File saved: {file_path}"
    )

    # ========================================================
    # 6. Check file size
    # ========================================================

    file_size = file_path.stat().st_size

    print(
        f"File size: {file_size} bytes"
    )

    if file_size == 0:

        file_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # ========================================================
    # 7. Ingest into RAG
    # ========================================================

    try:

        result = ingest_document(
            str(file_path),
            document_type,
        )

    except Exception as exc:

        print()
        print(
            f"DOCUMENT INGESTION ERROR: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Document processing failed: {exc}"
            ),
        )

    # ========================================================
    # 8. Return success
    # ========================================================

    print(
        "DOCUMENT UPLOAD SUCCESSFUL"
    )

    print("=" * 60)
    print()

    return {
        "success": True,
        "message": (
            "Document uploaded and processed successfully."
        ),
        "file_name": original_filename,
        "document_type": document_type,
        "file_size": file_size,
        "chunks_created": result.get(
            "chunks_created",
            0,
        ),
    }


# ============================================================
# PASTE JOB DESCRIPTION
# ============================================================

@router.post("/job-description")
async def add_job_description(
    request: JobDescriptionRequest,
):
    """
    Add a job description by pasting text.

    POST /documents/job-description
    """

    print()
    print("=" * 60)
    print("JOB DESCRIPTION TEXT")
    print("=" * 60)

    # ========================================================
    # 1. Validate
    # ========================================================

    if not request.text:

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    text = request.text.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    print(
        f"Job description length: {len(text)} characters"
    )

    # ========================================================
    # 2. Ingest into RAG
    # ========================================================

    try:

        result = ingest_text(
            text=text,
            document_type="job_description",
        )

    except Exception as exc:

        print(
            f"JOB DESCRIPTION ERROR: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Job description processing failed: {exc}"
            ),
        )

    # ========================================================
    # 3. Return success
    # ========================================================

    print(
        "JOB DESCRIPTION ADDED SUCCESSFULLY"
    )

    print("=" * 60)
    print()

    return {
        "success": True,
        "message": (
            "Job description added successfully."
        ),
        "document_type": "job_description",
        "chunks_created": result.get(
            "chunks_created",
            0,
        ),
    }