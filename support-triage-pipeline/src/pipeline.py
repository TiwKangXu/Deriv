from src.enums.pipeline_stage import (
    PipelineStage
)

from src.utils.state_manager import (
    StateManager
)

from src.stages.init_stage import (
    run_init_stage
)

from src.stages.load_inputs import (
    run_load_inputs_stage
)

from src.stages.normalize_tickets import (
    run_normalization_stage
)

from src.stages.predict_triage import (
    run_triage_prediction_stage
)

from src.stages.human_review import (
    run_human_review_stage
)

from src.stages.generate_final_queue import (
    run_generate_final_queue_stage
)

from src.stages.validate_outputs import (
    run_validation_stage
)

from src.stages.finalize_results import (
    run_finalize_results_stage
)


class SupportTriagePipeline:

    def __init__(self):

        self.state_manager = (
            StateManager()
        )

    def run(self):

        run_init_stage()

        self.state_manager.transition_to(
            PipelineStage.INPUTS_LOADED
        )

        run_load_inputs_stage()

        self.state_manager.transition_to(
            PipelineStage.TICKETS_NORMALIZED
        )

        run_normalization_stage()

        self.state_manager.transition_to(
            PipelineStage.TRIAGE_PREDICTED
        )

        run_triage_prediction_stage()

        self.state_manager.transition_to(
            PipelineStage.HUMAN_REVIEW_COMPLETE
        )

        run_human_review_stage()

        self.state_manager.transition_to(
            PipelineStage.FINAL_QUEUE_GENERATED
        )

        run_generate_final_queue_stage()

        self.state_manager.transition_to(
            PipelineStage.VALIDATION_COMPLETE
        )

        run_validation_stage()

        self.state_manager.transition_to(
            PipelineStage.RESULTS_FINALISED
        )

        run_finalize_results_stage()