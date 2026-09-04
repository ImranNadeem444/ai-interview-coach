from pathlib import Path
from uuid import uuid4

import edge_tts


# ============================================================
# Configuration
# ============================================================

# backend/
#   app/
#     services/
#       tts_service.py
#
# parent              -> services
# parent.parent       -> app
# parent.parent.parent -> backend

BASE_DIR = Path(__file__).resolve().parent.parent.parent

AUDIO_DIR = BASE_DIR / "audio"

AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Voice Configuration
# ============================================================

VOICE = "en-US-GuyNeural"


# ============================================================
# Internal Async TTS Function
# ============================================================

async def _generate_speech_async(
    text: str,
    output_path: Path,
) -> Path:
    """
    Generate an MP3 file using Edge TTS.

    This function is asynchronous, so it must be awaited.
    """

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
    )

    await communicate.save(
        str(output_path)
    )

    return output_path


# ============================================================
# Async Public Function
# ============================================================

async def generate_speech_async(
    text: str,
) -> str:
    """
    Generate speech asynchronously.

    IMPORTANT:
    Use this function inside async FastAPI routes.

    Example:

        audio_url = await generate_speech_async(
            "Tell me about yourself."
        )
    """

    # --------------------------------------------------------
    # Validate text
    # --------------------------------------------------------

    if not text or not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    # --------------------------------------------------------
    # Create unique filename
    # --------------------------------------------------------

    filename = (
        f"question_{uuid4().hex}.mp3"
    )

    output_path = AUDIO_DIR / filename

    print()
    print("[TTS] Generating question audio...")
    print(f"[TTS] Text: {text}")
    print(f"[TTS] Output: {output_path}")

    # --------------------------------------------------------
    # Generate speech
    # --------------------------------------------------------

    try:

        await _generate_speech_async(
            text=text,
            output_path=output_path,
        )

    except Exception as exc:

        print(
            f"[TTS] ERROR: {exc}"
        )

        raise RuntimeError(
            f"TTS generation failed: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Verify file exists
    # --------------------------------------------------------

    if not output_path.exists():

        raise RuntimeError(
            "TTS completed but audio file "
            "was not created."
        )

    # --------------------------------------------------------
    # Verify file is not empty
    # --------------------------------------------------------

    file_size = output_path.stat().st_size

    if file_size == 0:

        raise RuntimeError(
            "TTS created an empty audio file."
        )

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print(
        f"[TTS] Audio created: {output_path}"
    )

    print(
        f"[TTS] Size: {file_size} bytes"
    )

    # Return URL path, NOT Windows filesystem path
    return f"/audio/{filename}"


# ============================================================
# Synchronous Public Function
# ============================================================

def generate_speech(
    text: str,
) -> str:
    """
    Generate speech synchronously.

    Use this only from normal synchronous Python code.

    Example:

        generate_speech("Hello Imran")

    DO NOT use this inside an async FastAPI endpoint.
    """

    import asyncio

    # --------------------------------------------------------
    # Validate text
    # --------------------------------------------------------

    if not text or not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    # --------------------------------------------------------
    # Create unique filename
    # --------------------------------------------------------

    filename = (
        f"question_{uuid4().hex}.mp3"
    )

    output_path = AUDIO_DIR / filename

    print()
    print("[TTS] Generating question audio...")
    print(f"[TTS] Text: {text}")
    print(f"[TTS] Output: {output_path}")

    # --------------------------------------------------------
    # Run async TTS from synchronous code
    # --------------------------------------------------------

    try:

        asyncio.run(
            _generate_speech_async(
                text=text,
                output_path=output_path,
            )
        )

    except Exception as exc:

        print(
            f"[TTS] ERROR: {exc}"
        )

        raise RuntimeError(
            f"TTS generation failed: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Verify file exists
    # --------------------------------------------------------

    if not output_path.exists():

        raise RuntimeError(
            "TTS completed but audio file "
            "was not created."
        )

    # --------------------------------------------------------
    # Verify file is not empty
    # --------------------------------------------------------

    file_size = output_path.stat().st_size

    if file_size == 0:

        raise RuntimeError(
            "TTS created an empty audio file."
        )

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print(
        f"[TTS] Audio created: {output_path}"
    )

    print(
        f"[TTS] Size: {file_size} bytes"
    )

    return f"/audio/{filename}"