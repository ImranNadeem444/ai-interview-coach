from app.services.retrieval_service import (
    retrieve_resume,
    retrieve_job_description,
)


def main():

    # =========================================================
    # RESUME SEARCH
    # =========================================================

    print("\n" + "=" * 30)
    print("RESUME SEARCH")
    print("=" * 30)

    resume_results = retrieve_resume(
        query="What AI, machine learning, LLM, and software development skills does the candidate have?",
        n_results=3,
    )

    if not resume_results:
        print("No resume results found.")
    else:
        for i, result in enumerate(resume_results, start=1):
            print(f"\n--- Result {i} ---")
            print(result)


    # =========================================================
    # JOB DESCRIPTION SEARCH
    # =========================================================

    print("\n" + "=" * 30)
    print("JOB DESCRIPTION SEARCH")
    print("=" * 30)

    job_results = retrieve_job_description(
        query="What skills, experience, technologies, and responsibilities are required for this job?",
        n_results=5,
    )

    if not job_results:
        print("No job description results found.")
    else:
        for i, result in enumerate(job_results, start=1):
            print(f"\n--- Result {i} ---")
            print(result)


if __name__ == "__main__":
    main()