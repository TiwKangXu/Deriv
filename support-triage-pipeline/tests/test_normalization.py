from src.services.normalization_service import NormalizationService


def test_build_text_for_model():
    result = NormalizationService.build_text_for_model(
        "Login Issue",
        "I cannot access my account."
    )

    expected = (
        "Subject: Login Issue\n"
        "Message: I cannot access my account."
    )

    assert result == expected


def test_char_count():
    service = NormalizationService()

    ticket = {
        "ticket_id": "T-001",
        "subject": "Hello",
        "message": "World",
        "channel": "email",
        "created_at": "2026-01-01"
    }

    normalized = service.normalize_ticket(ticket)

    assert normalized["char_count"] == len(
        normalized["text_for_model"]
    )