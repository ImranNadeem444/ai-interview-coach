from app.chains.evaluation_chain import evaluate_answer


def main():

    question = """
    Can you explain your experience with FastAPI
    and how you used it in your AI projects?
    """

    answer = """
    I used FastAPI to build the backend for Mentimotive.
    I created API endpoints for the AI services and used
    asynchronous endpoints. I also implemented JWT
    authentication and used Docker for deployment.
    """

    print("=" * 50)
    print("STRUCTURED ANSWER EVALUATION")
    print("=" * 50)

    evaluation = evaluate_answer(
        question=question,
        answer=answer,
    )

    print("\nScore:")
    print(evaluation.score)

    print("\nTechnical Accuracy:")
    print(evaluation.technical_accuracy)

    print("\nRelevance:")
    print(evaluation.relevance)

    print("\nStrengths:")

    for strength in evaluation.strengths:
        print(f"- {strength}")

    print("\nWeaknesses:")

    for weakness in evaluation.weaknesses:
        print(f"- {weakness}")

    print("\nImprovement:")
    print(evaluation.improvement)

    print("\nFollow-up Needed:")
    print(evaluation.follow_up_needed)


if __name__ == "__main__":
    main()