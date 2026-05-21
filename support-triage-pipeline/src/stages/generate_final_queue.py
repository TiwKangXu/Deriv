import json
from pathlib import Path

from src.models.queue_item import (
    FinalQueueItem
)

from src.services.summary_service import (
    SummaryService
)


TRIAGE_PREDICTIONS_PATH = Path(
    "triage_predictions.json"
)

REVIEW_OVERRIDES_PATH = Path(
    "review_overrides.json"
)

FINAL_QUEUE_PATH = Path(
    "final_queue.json"
)

QUEUE_SUMMARY_PATH = Path(
    "queue_summary.md"
)


def load_json(path: Path):

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data):

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def save_markdown(path: Path, content: str):

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def build_override_lookup(
    overrides: list
):

    return {
        item["ticket_id"]: item
        for item in overrides
    }


def build_final_queue(
    predictions: list,
    override_lookup: dict
):

    final_queue = []

    for prediction in predictions:

        ticket_id = prediction[
            "ticket_id"
        ]

        was_overridden = (
            ticket_id
            in override_lookup
        )

        queue_item = FinalQueueItem(
            ticket_id=ticket_id,

            final_category=prediction[
                "category"
            ],

            final_priority=prediction[
                "priority"
            ],

            final_route_to=prediction[
                "route_to"
            ],

            suggested_reply=prediction[
                "suggested_reply"
            ],

            was_overridden=was_overridden
        )

        final_queue.append(
            queue_item.model_dump()
        )

    return final_queue


def run_generate_final_queue_stage():

    predictions = load_json(
        TRIAGE_PREDICTIONS_PATH
    )

    overrides = load_json(
        REVIEW_OVERRIDES_PATH
    )

    override_lookup = (
        build_override_lookup(
            overrides
        )
    )

    final_queue = (
        build_final_queue(
            predictions,
            override_lookup
        )
    )

    save_json(
        FINAL_QUEUE_PATH,
        final_queue
    )

    summary = (
        SummaryService.build_summary(
            final_queue,
            overrides
        )
    )

    save_markdown(
        QUEUE_SUMMARY_PATH,
        summary
    )

    print(
        f"[FINAL QUEUE] Saved "
        f"{len(final_queue)} tickets"
    )

    print(
        f"[SUMMARY] Saved "
        f"{QUEUE_SUMMARY_PATH}"
    )

    return final_queue