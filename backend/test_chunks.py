from app.rag.loaders import load_pdf
from app.rag.chunker import chunk_text


file_path = "../uploads/Imran_Nadeem_(Resume).pdf"

text = load_pdf(file_path)

chunks = chunk_text(
    text,
    chunk_size=800,
    chunk_overlap=100,
)

print(f"\nTotal chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):

    print("\n" + "=" * 60)
    print(f"CHUNK {i}")
    print(f"SECTION: {chunk['section']}")
    print("=" * 60)

    print(chunk["text"])