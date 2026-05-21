from pathlib import Path


def ensure_file_exists(
    file_path: str
):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"{file_path} not found"
        )


def ensure_required_inputs():

    ensure_file_exists(
        "tickets.json"
    )

    ensure_file_exists(
        "triage_config.json"
    )