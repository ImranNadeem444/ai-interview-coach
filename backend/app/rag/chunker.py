import re


SECTION_NAMES = [
    "PROFESSIONAL SUMMARY",
    "SKILLS / STRENGTHS",
    "EXPERIENCE",
    "PROJECTS",
    "EDUCATION",
    "CERTIFICATIONS",
]


def detect_sections(text: str) -> list[dict]:
    """
    Detect major CV sections and return their text.
    """

    lines = text.splitlines()

    sections = []
    current_section = "HEADER"
    current_lines = []

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        matched_section = None

        for section_name in SECTION_NAMES:
            if clean_line.upper() == section_name:
                matched_section = section_name
                break

        if matched_section:
            if current_lines:
                sections.append(
                    {
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                    }
                )

            current_section = matched_section
            current_lines = []

        else:
            current_lines.append(clean_line)

    # Add final section
    if current_lines:
        sections.append(
            {
                "section": current_section,
                "text": "\n".join(current_lines).strip(),
            }
        )

    return sections


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def chunk_section(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> list[str]:
    """
    Split one section into meaningful chunks.
    """

    sentences = split_into_sentences(text)

    if not sentences:
        return []

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        if (
            current_chunk
            and current_length + sentence_length > chunk_size
        ):
            chunks.append(" ".join(current_chunk))

            # Keep previous context for overlap
            overlap = []
            overlap_length = 0

            for previous in reversed(current_chunk):
                if overlap_length + len(previous) > chunk_overlap:
                    break

                overlap.insert(0, previous)
                overlap_length += len(previous)

            current_chunk = overlap
            current_length = overlap_length

        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> list[dict]:
    """
    Create section-aware chunks.

    Each chunk contains:
    - section
    - text
    """

    sections = detect_sections(text)

    chunks = []

    for section in sections:

        section_chunks = chunk_section(
            section["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk in section_chunks:
            chunks.append(
                {
                    "section": section["section"],
                    "text": chunk,
                }
            )

    return chunks