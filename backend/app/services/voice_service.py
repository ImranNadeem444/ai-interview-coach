from pathlib import Path

from faster_whisper import WhisperModel
import pyttsx3


# ============================================================
# Whisper
# ============================================================

# Load Whisper once when the service starts.
# This avoids loading the model for every request.

whisper_model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8",
)


def transcribe_audio(audio_path: str) -> str:
    """
    Convert an audio file into text using Faster-Whisper.
    """

    path = Path(audio_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    segments, info = whisper_model.transcribe(
        str(path),
        beam_size=5,
    )

    transcript = []

    for segment in segments:

        text = segment.text.strip()

        if text:
            transcript.append(text)

    return " ".join(transcript).strip()


# ============================================================
# Text-to-Speech
# ============================================================

def text_to_speech(
    text: str,
    output_path: str,
) -> str:
    """
    Convert text into a WAV audio file using
    the Windows offline speech engine.
    """

    if not text or not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    output = Path(output_path)

    # Create parent directory if necessary.
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    engine = pyttsx3.init()

    # --------------------------------------------------------
    # Voice settings
    # --------------------------------------------------------

    engine.setProperty(
        "rate",
        175,
    )

    engine.setProperty(
        "volume",
        1.0,
    )

    # --------------------------------------------------------
    # Generate speech
    # --------------------------------------------------------

    engine.save_to_file(
        text,
        str(output),
    )

    engine.runAndWait()

    engine.stop()

    # --------------------------------------------------------
    # Verify output
    # --------------------------------------------------------

    if not output.exists():
        raise RuntimeError(
            "Text-to-speech failed to create audio file."
        )

    return str(output)