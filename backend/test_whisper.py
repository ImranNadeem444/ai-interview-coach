from faster_whisper import WhisperModel


def main():
    print("=" * 60)
    print("WHISPER SPEECH-TO-TEXT TEST")
    print("=" * 60)

    audio_file = input("\nEnter audio file path: ").strip()

    if not audio_file:
        print("No audio file provided.")
        return

    print("\nLoading Whisper model...")
    print("The first run may download the model.\n")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
    )

    print("Transcribing...\n")

    segments, info = model.transcribe(
        audio_file,
        beam_size=5,
    )

    print("Detected language:", info.language)
    print("Language probability:", round(info.language_probability, 3))
    print("\nTranscript:")
    print("-" * 60)

    full_text = []

    for segment in segments:
        text = segment.text.strip()

        if text:
            print(text)
            full_text.append(text)

    print("-" * 60)
    print("\nFinal transcript:")
    print(" ".join(full_text))

    print("\n" + "=" * 60)
    print("WHISPER TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()