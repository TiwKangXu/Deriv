from src.utils.file_utils import (
    ensure_required_inputs
)


def run_load_inputs_stage():

    ensure_required_inputs()

    print(
        "[INPUTS] "
        "tickets.json loaded"
    )

    print(
        "[INPUTS] "
        "triage_config.json loaded"
    )