import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from src.models.override import ReviewOverride
from src.services.routing_service import RoutingService


TRIAGE_PREDICTIONS_PATH = Path(
    "triage_predictions.json"
)

TRIAGE_CONFIG_PATH = Path(
    "triage_config.json"
)

REVIEW_OVERRIDES_PATH = Path(
    "review_overrides.json"
)


console = Console()


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def display_predictions(predictions: list):

    table = Table(
        title="Human Review Checkpoint"
    )

    table.add_column("Ticket ID")
    table.add_column("Category")
    table.add_column("Priority")
    table.add_column("Route")

    for prediction in predictions:

        table.add_row(
            prediction["ticket_id"],
            prediction["category"],
            prediction["priority"],
            prediction["route_to"]
        )

    console.print(table)


def apply_override(
    prediction: dict,
    new_category: str,
    new_priority: str,
    routing_rules: dict
):

    prediction["category"] = new_category
    prediction["priority"] = new_priority

    prediction["route_to"] = (
        RoutingService.get_route(
            new_category,
            routing_rules
        )
    )

    return prediction


def run_human_review_stage():

    predictions = load_json(
        TRIAGE_PREDICTIONS_PATH
    )

    triage_config = load_json(
        TRIAGE_CONFIG_PATH
    )

    allowed_categories = (
        triage_config["allowed_categories"]
    )

    allowed_priorities = (
        triage_config["allowed_priorities"]
    )

    routing_rules = (
        triage_config["routing_rules"]
    )

    prediction_map = {
        item["ticket_id"]: item
        for item in predictions
    }

    overrides = []

    display_predictions(predictions)

    console.print(
        "\nEnter any overrides as:"
    )

    console.print(
        "ticket_id,category,priority"
    )

    console.print(
        "Press Enter on an empty line when done.\n"
    )

    while True:

        user_input = input("> ").strip()

        if not user_input:
            break

        try:

            parts = [
                item.strip()
                for item in user_input.split(",")
            ]

            if len(parts) != 3:
                raise ValueError(
                    "Expected 3 values"
                )

            ticket_id = parts[0]
            new_category = parts[1]
            new_priority = parts[2]

            if ticket_id not in prediction_map:
                raise ValueError(
                    f"Unknown ticket_id: {ticket_id}"
                )

            if (
                new_category
                not in allowed_categories
            ):
                raise ValueError(
                    f"Invalid category: {new_category}"
                )

            if (
                new_priority
                not in allowed_priorities
            ):
                raise ValueError(
                    f"Invalid priority: {new_priority}"
                )

            prediction = prediction_map[
                ticket_id
            ]

            override = ReviewOverride(
                ticket_id=ticket_id,

                old_category=prediction[
                    "category"
                ],

                new_category=new_category,

                old_priority=prediction[
                    "priority"
                ],

                new_priority=new_priority
            )

            overrides.append(
                override.model_dump()
            )

            updated_prediction = (
                apply_override(
                    prediction,
                    new_category,
                    new_priority,
                    routing_rules
                )
            )

            prediction_map[
                ticket_id
            ] = updated_prediction

            console.print(
                f"[green]Override applied for "
                f"{ticket_id} | "
                f"{override.old_category}"
                f" -> "
                f"{override.new_category} | "
                f"{override.old_priority}"
                f" -> "
                f"{override.new_priority}"
                f"[/green]"
            )

        except Exception as error:

            console.print(
                f"[red]{error}[/red]"
            )

    updated_predictions = list(
        prediction_map.values()
    )

    save_json(
        TRIAGE_PREDICTIONS_PATH,
        updated_predictions
    )

    if not overrides:
        console.print(
            "[yellow]No overrides made.[/yellow]"
        )

    save_json(
        REVIEW_OVERRIDES_PATH,
        overrides
    )

    console.print(
        "\n[bold cyan]"
        "review_overrides.json"
        "[/bold cyan]"
    )

    console.print_json(
        data=overrides
    )

    console.print(
        f"\n[bold green]"
        f"Saved {len(overrides)} overrides"
        f"[/bold green]"
    )

    return updated_predictions