from app.services.context_service import (
    build_interview_context,
)


context = build_interview_context(
    query=(
        "What skills and experience should be "
        "evaluated for this AI Developer position?"
    ),
    n_results=3,
)


print("\n==============================")
print("RESUME CONTEXT")
print("==============================")

print(context["resume_context"])


print("\n==============================")
print("JOB DESCRIPTION CONTEXT")
print("==============================")

print(context["job_description_context"])