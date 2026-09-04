from pydantic import BaseModel, Field


class InterviewReport(BaseModel):
    overall_score: float = Field(
        ge=1,
        le=10,
        description="Overall interview score from 1 to 10."
    )

    technical_performance: str
    communication: str

    strengths: list[str]
    weaknesses: list[str]

    skills_demonstrated: list[str]
    skills_to_improve: list[str]

    job_fit: str
    recommendations: list[str]