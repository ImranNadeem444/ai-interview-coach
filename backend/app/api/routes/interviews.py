from uuid import UUID
from pathlib import Path
import tempfile

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.interview_service import InterviewSession
from app.services.voice_service import transcribe_audio
from app.services.tts_service import generate_speech_async


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


# ============================================================
# Database Dependency
# ============================================================

def get_db():
    """
    Create a database session for one API request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# Request Schemas
# ============================================================

class CreateInterviewRequest(BaseModel):
    """
    Information required to start an interview.
    """

    resume_query: str = Field(
        ...,
        min_length=1,
        description="Candidate resume or extracted resume context.",
    )

    job_description: str = Field(
        ...,
        min_length=1,
        description="Job description for the interview.",
    )


class SubmitAnswerRequest(BaseModel):
    """
    Text answer to an interview question.
    """

    answer: str = Field(
        ...,
        min_length=1,
        description="Candidate answer.",
    )


# ============================================================
# Create Interview
# ============================================================

@router.post("/")
async def create_interview(
    request: CreateInterviewRequest,
    db: Session = Depends(get_db),
):
    """
    Start a new interview.

    Flow:

        Resume + Job Description
                ↓
        InterviewSession
                ↓
        First Question
                ↓
        Edge TTS
                ↓
        Question Audio
    """

    print()
    print("=" * 70)
    print("STARTING NEW INTERVIEW")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # 1. Create interview session
        # ----------------------------------------------------

        print("[1/3] Creating interview session...")

        session = InterviewSession(
            db=db,
            resume_query=request.resume_query,
            job_description=request.job_description,
        )

        print(
            f"Interview ID: {session.interview_id}"
        )

        # ----------------------------------------------------
        # 2. Generate first question
        # ----------------------------------------------------

        print("[2/3] Generating first question...")

        first_question = session.get_next_question()

        print(
            f"First question: {first_question}"
        )

        # ----------------------------------------------------
        # 3. Generate first question audio
        # ----------------------------------------------------

        print("[3/3] Generating first question audio...")

        audio_path = await generate_speech_async(
            first_question
        )

        audio_filename = Path(
            audio_path
        ).name

        question_audio = (
            f"/audio/{audio_filename}"
        )

        print(
            f"Question audio URL: {question_audio}"
        )

        print()
        print("INTERVIEW CREATED SUCCESSFULLY")

        return {
            "interview_id": str(
                session.interview_id
            ),
            "question": first_question,
            "question_audio": question_audio,
            "status": "in_progress",
        }

    except Exception as exc:

        print(
            f"ERROR CREATING INTERVIEW: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Submit Text Answer
# ============================================================

@router.post("/{interview_id}/answer")
async def submit_answer(
    interview_id: UUID,
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
):
    """
    Submit a text answer.

    Flow:

        Candidate Answer
              ↓
        Evaluation
              ↓
        Next Question
              ↓
        Edge TTS
              ↓
        Next Question Audio
    """

    try:

        # ----------------------------------------------------
        # Load interview
        # ----------------------------------------------------

        session = InterviewSession.from_database(
            db=db,
            interview_id=interview_id,
        )

        # ----------------------------------------------------
        # Evaluate answer
        # ----------------------------------------------------

        evaluation = session.add_candidate_answer(
            request.answer
        )

        # ----------------------------------------------------
        # Generate next question
        # ----------------------------------------------------

        next_question = session.get_next_question()

        # ----------------------------------------------------
        # Generate next question audio
        # ----------------------------------------------------

        audio_path = await generate_speech_async(
            next_question
        )

        audio_filename = Path(
            audio_path
        ).name

        question_audio = (
            f"/audio/{audio_filename}"
        )

        return {
            "interview_id": str(
                session.interview_id
            ),
            "evaluation": evaluation,
            "next_question": next_question,
            "question_audio": question_audio,
            "status": "in_progress",
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Submit Voice Answer
# ============================================================

@router.post("/{interview_id}/voice-answer")
async def submit_voice_answer(
    interview_id: UUID,
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Receive candidate's voice answer.

    Complete flow:

        Audio
          ↓
        Faster-Whisper
          ↓
        Transcript
          ↓
        InterviewSession
          ↓
        Evaluation
          ↓
        Next Question
          ↓
        Edge TTS
          ↓
        Question Audio
    """

    print()
    print("=" * 70)
    print("VOICE ANSWER REQUEST RECEIVED")
    print("=" * 70)

    print(
        f"Interview ID: {interview_id}"
    )

    print(
        f"Filename: {audio.filename}"
    )

    print(
        f"Content type: {audio.content_type}"
    )

    if not audio.filename:

        raise HTTPException(
            status_code=400,
            detail="No audio file provided.",
        )

    suffix = (
        Path(audio.filename).suffix
        or ".webm"
    )

    temp_path = None

    try:

        # ----------------------------------------------------
        # 1. Read uploaded audio
        # ----------------------------------------------------

        print("[1/6] Reading uploaded audio...")

        audio_bytes = await audio.read()

        if not audio_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty.",
            )

        print(
            f"Received {len(audio_bytes)} bytes"
        )

        # ----------------------------------------------------
        # 2. Save temporary audio
        # ----------------------------------------------------

        print("[2/6] Saving temporary audio...")

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(audio_bytes)

            temp_path = temp_file.name

        print(
            f"Temporary audio: {temp_path}"
        )

        # ----------------------------------------------------
        # 3. Faster-Whisper
        # ----------------------------------------------------

        print("[3/6] Starting Faster-Whisper...")

        print(
            "Please wait while the audio is transcribed..."
        )

        transcript = transcribe_audio(
            temp_path
        )

        print("Whisper finished.")

        print(
            f"Transcript: {transcript}"
        )

        if not transcript:

            raise HTTPException(
                status_code=400,
                detail="Could not detect speech in the audio.",
            )

        # ----------------------------------------------------
        # 4. Load interview session
        # ----------------------------------------------------

        print(
            "[4/6] Loading interview session..."
        )

        session = InterviewSession.from_database(
            db=db,
            interview_id=interview_id,
        )

        print(
            "Interview session loaded."
        )

        # ----------------------------------------------------
        # 5. Evaluate answer
        # ----------------------------------------------------

        print(
            "[5/6] Evaluating candidate answer..."
        )

        evaluation = session.add_candidate_answer(
            transcript
        )

        print(
            "Answer evaluation completed."
        )

        # ----------------------------------------------------
        # Generate next question
        # ----------------------------------------------------

        print(
            "Generating next interview question..."
        )

        next_question = session.get_next_question()

        print(
            f"Next question: {next_question}"
        )

        # ----------------------------------------------------
        # 6. Generate next question audio
        # ----------------------------------------------------

        print(
            "[6/6] Generating question audio..."
        )

        # IMPORTANT:
        # This endpoint is async, so we MUST await
        # the async TTS function.

        audio_path = await generate_speech_async(
            next_question
        )

        audio_filename = Path(
            audio_path
        ).name

        question_audio = (
            f"/audio/{audio_filename}"
        )

        print(
            f"Question audio URL: {question_audio}"
        )

        print()
        print(
            "VOICE ANSWER PROCESSED SUCCESSFULLY"
        )

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "interview_id": str(
                session.interview_id
            ),
            "transcript": transcript,
            "evaluation": evaluation,
            "next_question": next_question,
            "question_audio": question_audio,
            "status": "in_progress",
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except HTTPException:

        raise

    except Exception as exc:

        print(
            f"VOICE ANSWER ERROR: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    finally:

        # ----------------------------------------------------
        # Delete temporary candidate audio
        # ----------------------------------------------------

        if temp_path:

            try:

                Path(temp_path).unlink(
                    missing_ok=True
                )

            except Exception:

                pass


# ============================================================
# Get Interview
# ============================================================

@router.get("/{interview_id}")
def get_interview(
    interview_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get current interview state.
    """

    try:

        session = InterviewSession.from_database(
            db=db,
            interview_id=interview_id,
        )

        return session.get_interview_state()

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )