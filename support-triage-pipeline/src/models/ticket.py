from pydantic import BaseModel


class Ticket(BaseModel):
    ticket_id: str
    customer_id: str
    subject: str
    message: str
    channel: str
    created_at: str


class NormalizedTicket(BaseModel):
    ticket_id: str
    subject: str
    message: str
    channel: str
    created_at: str
    text_for_model: str
    char_count: int