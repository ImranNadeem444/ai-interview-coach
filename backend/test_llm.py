from app.services.llm_service import generate_text


def main():
    prompt = """
You are an AI interview coach.

Say hello to the candidate and explain in one sentence
that you will conduct their interview.
"""

    response = generate_text(prompt)

    print("\n==============================")
    print("GEMINI RESPONSE")
    print("==============================")
    print(response)


if __name__ == "__main__":
    main()