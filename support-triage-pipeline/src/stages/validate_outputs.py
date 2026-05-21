from pathlib import Path


REQUIRED_OUTPUTS = [
    "normalized_tickets.json",
    "triage_predictions.json",
    "review_overrides.json",
    "final_queue.json",
    "queue_summary.md"
]


def run_validation_stage():

    missing_files = []

    for file_name in REQUIRED_OUTPUTS:

        if not Path(file_name).exists():

            missing_files.append(
                file_name
            )

    if missing_files:

        raise FileNotFoundError(
            f"Missing outputs: "
            f"{missing_files}"
        )

    print(
        "[VALIDATION] "
        "All required outputs exist"
    )