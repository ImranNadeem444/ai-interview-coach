from app.services.voice_service import text_to_speech


print("=" * 60)
print("TEXT-TO-SPEECH TEST")
print("=" * 60)

output_file = "test_question.wav"

text = (
    "Hi Imran, could you start by telling me "
    "a little about yourself, your background, "
    "and what led you to pursue AI and machine learning?"
)

print()
print("Generating speech...")
print()

result = text_to_speech(
    text=text,
    output_path=output_file,
)

print("Audio generated successfully:")
print(result)

print()
print("=" * 60)
print("TTS TEST COMPLETE")
print("=" * 60)