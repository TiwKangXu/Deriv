from src.enums.pipeline_stage import (
    PipelineStage
)


class StateManager:

    def __init__(self):

        self.current_stage = (
            PipelineStage.INIT
        )

    def transition_to(
        self,
        new_stage: PipelineStage
    ):

        self.current_stage = new_stage

        print(
            f"\n[PIPELINE] "
            f"{self.current_stage.value}"
        )

    def get_stage(self):

        return self.current_stage