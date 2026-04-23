from pydantic import BaseModel, Field
from typing import Literal


# ============================================================
# INPUT MODEL (Frontend → Backend)
# ============================================================

class SimulationInput(BaseModel):
    attendance: float = Field(
        ...,
        ge=0,
        le=100,
        description="Attendance percentage (0–100)"
    )

    assignments: int = Field(
        ...,
        ge=0,
        le=14,
        description="Number of assignments per week (0–14)"
    )

    examGap: int = Field(
        ...,
        ge=0,
        le=30,
        description="Gap between exams in days (0–30)"
    )

    sleep: float = Field(
        ...,
        ge=0,
        le=12,
        description="Average sleep hours per day (0–12)"
    )

    cgpa: float = Field(
        ...,
        ge=0,
        le=10,
        description="Current CGPA (0–10)"
    )

    class Config:
        schema_extra = {
            "example": {
                "attendance": 85,
                "assignments": 4,
                "examGap": 10,
                "sleep": 7,
                "cgpa": 7.5
            }
        }


# ============================================================
# OUTPUT MODEL (Backend → Frontend)
# ============================================================

class SimulationOutput(BaseModel):
    stress: int = Field(
        ...,
        ge=0,
        le=100,
        description="Predicted stress level (0–100)"
    )

    engagement: int = Field(
        ...,
        ge=0,
        le=100,
        description="Predicted engagement level (0–100)"
    )

    risk_prob: int = Field(
        ...,
        ge=0,
        le=100,
        description="Dropout risk probability percentage"
    )

    risk_level: Literal["Low", "Medium", "High"] = Field(
        ...,
        description="Categorical dropout risk level"
    )

    recommended_sleep: float = Field(
        ...,
        ge=0,
        le=12,
        description="Recommended sleep hours if assignments increase by 1"
    )

    sleep_increase: float = Field(
        ...,
        ge=0,
        description="Additional sleep hours needed"
    )

    class Config:
        schema_extra = {
            "example": {
                "stress": 62,
                "engagement": 74,
                "risk_prob": 28,
                "risk_level": "Low",
                "recommended_sleep": 8,
                "sleep_increase": 1
            }
        }