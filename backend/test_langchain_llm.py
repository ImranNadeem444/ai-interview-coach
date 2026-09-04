from app.services.llm_service import llm


def main():
    response = llm.invoke(
        "Say hello and explain in one sentence what an AI interview coach does."
    )

    print("==============================")
    print("LANGCHAIN LLM RESPONSE")
    print("==============================")
    print(response.content)


if __name__ == "__main__":
    main()