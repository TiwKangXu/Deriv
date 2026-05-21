from pydantic import BaseModel, Field


class TriagePrediction(BaseModel):
    ticket_id: str

    category: str
    priority: str

    reason: str
    suggested_reply: str

    route_to: str

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0
    )