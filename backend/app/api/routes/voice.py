from pathlib import Path
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.voice_service import transcribe_audio


router = APIRouter(
    prefix="/voice",
    tags=["Voice"],
)


@router.post("/transcribe")
async def transcribe_voice(
    audio: UploadFile = File(...),
):
    """
    Receive an audio file and convert it to text using
    local Faster-Whisper.
    """

    if not audio.filename:
        raise HTTPException(
            status_code=400,
            detail="No audio file provided.",
        )

    suffix = Path(audio.filename).suffix or ".wav"

    temp_path = None

    try:
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty.",
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        transcript = transcribe_audio(temp_path)

        return {
            "success": True,
            "filename": audio.filename,
            "text": transcript,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Voice transcription failed: {str(e)}",
        )

    finally:
        if temp_path:
            try:
                Path(temp_path).unlink(missing_ok=True)
            except Exception:
                pass