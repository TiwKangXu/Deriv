import json
from pathlib import Path
from typing import List, Dict


class NormalizationService:
    def __init__(
        self,
        input_path: str = "tickets.json",
        output_path: str = "normalized_tickets.json",
    ):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

    def load_tickets(self) -> List[Dict]:
        if not self.input_path.exists():
            raise FileNotFoundError(f"{self.input_path} not found")

        with open(self.input_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def build_text_for_model(subject: str, message: str) -> str:
        """
        Deterministic preprocessing before any LLM call.
        """
        subject = subject.strip()
        message = message.strip()

        return f"Subject: {subject}\nMessage: {message}"

    def normalize_ticket(self, ticket: Dict) -> Dict:
        text_for_model = self.build_text_for_model(
            ticket.get("subject", ""),
            ticket.get("message", "")
        )

        return {
            "ticket_id": ticket.get("ticket_id", "").strip(),
            "subject": ticket.get("subject", "").strip(),
            "message": ticket.get("message", "").strip(),
            "channel": ticket.get("channel", "").strip(),
            "created_at": ticket.get("created_at", "").strip(),
            "text_for_model": text_for_model,
            "char_count": len(text_for_model)
        }

    def normalize_all_tickets(self) -> List[Dict]:
        raw_tickets = self.load_tickets()

        normalized_tickets = [
            self.normalize_ticket(ticket)
            for ticket in raw_tickets
        ]

        return normalized_tickets

    def save_normalized_tickets(self, normalized_tickets: List[Dict]) -> None:
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(normalized_tickets, file, indent=2)

    def run(self) -> List[Dict]:
        normalized_tickets = self.normalize_all_tickets()
        self.save_normalized_tickets(normalized_tickets)

        print(
            f"[NORMALIZATION] Saved "
            f"{len(normalized_tickets)} normalized tickets "
            f"to {self.output_path}"
        )

        return normalized_tickets