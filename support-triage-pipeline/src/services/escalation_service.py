from typing import List, Dict


class EscalationService:
    @staticmethod
    def generate_escalations(
        predictions: List[Dict]
    ) -> List[Dict]:

        escalations = []

        for prediction in predictions:
            should_escalate = (
                prediction["category"] == "other"
                or prediction.get("confidence", 1.0) < 0.60
            )

            if should_escalate:
                escalations.append(prediction)

        return escalations