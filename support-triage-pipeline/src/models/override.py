from pydantic import BaseModel


class ReviewOverride(BaseModel):
    ticket_id: str

    old_category: str
    new_category: str

    old_priority: str
    new_priority: str