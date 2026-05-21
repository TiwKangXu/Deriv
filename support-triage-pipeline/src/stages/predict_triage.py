import json
from pathlib import Path

from src.llm.client import OpenAIClient
from src.llm.prompts import build_triage_prompt

from src.services.routing_service import RoutingService
from src.services.escalation_service import EscalationService


NORMALIZED_TICKETS_PATH = Path(
    "normalized_tickets.json"
)

TRIAGE_CONFIG_PATH = Path(
    "triage_config.json"
)

OUTPUT_PATH = Path(
    "triage_predictions.json"
)

ESCALATIONS_PATH = Path(
    "escalations.json"
)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_prediction(
    prediction: dict,
    triage_config: dict
) -> dict:

    allowed_categories = (
        triage_config["allowed_categories"]
    )

    allowed_priorities = (
        triage_config["allowed_priorities"]
    )

    routing_rules = (
        triage_config["routing_rules"]
    )

    if prediction["category"] not in allowed_categories:
        prediction["category"] = "other"

    if prediction["priority"] not in allowed_priorities:
        prediction["priority"] = "normal"

    prediction["route_to"] = (
        RoutingService.get_route(
            prediction["category"],
            routing_rules
        )
    )

    return prediction


def fallback_prediction(
    ticket_id: str
) -> dict:

    return {
        "ticket_id": ticket_id,
        "category": "other",
        "priority": "normal",
        "reason": (
            "Malformed or missing prediction."
        ),
        "suggested_reply": (
            "Thank you for contacting support. "
            "Your issue has been routed for "
            "manual review."
        ),
        "route_to": "manual_review_queue",
        "confidence": 0.0
    }


def save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def run_triage_prediction_stage():

    normalized_tickets = load_json(
        NORMALIZED_TICKETS_PATH
    )

    triage_config = load_json(
        TRIAGE_CONFIG_PATH
    )

    prompt = build_triage_prompt(
        normalized_tickets,
        triage_config
    )

    client = OpenAIClient().get_client()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict JSON API."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_content = (
        response.choices[0]
        .message
        .content
    )

    parsed = json.loads(raw_content)

    predictions = parsed.get(
        "predictions",
        parsed
    )

    validated_predictions = []

    prediction_map = {
        item["ticket_id"]: item
        for item in predictions
        if "ticket_id" in item
    }

    for ticket in normalized_tickets:

        ticket_id = ticket["ticket_id"]

        prediction = prediction_map.get(ticket_id)

        if not prediction:
            prediction = fallback_prediction(
                ticket_id
            )

        prediction = validate_prediction(
            prediction,
            triage_config
        )

        validated_predictions.append(
            prediction
        )

    save_json(
        OUTPUT_PATH,
        validated_predictions
    )

    escalations = (
        EscalationService
        .generate_escalations(
            validated_predictions
        )
    )

    save_json(
        ESCALATIONS_PATH,
        escalations
    )

    print(
        f"[TRIAGE] Saved "
        f"{len(validated_predictions)} "
        f"predictions"
    )

    print(
        f"[ESCALATIONS] Saved "
        f"{len(escalations)} "
        f"escalations"
    )

    return validated_predictions