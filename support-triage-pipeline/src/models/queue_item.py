from pydantic import BaseModel


class FinalQueueItem(BaseModel):
    ticket_id: str

    final_category: str
    final_priority: str
    final_route_to: str

    suggested_reply: str

    was_overridden: bool