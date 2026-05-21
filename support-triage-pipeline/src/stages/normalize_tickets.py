from src.services.normalization_service import NormalizationService


def run_normalization_stage():
    service = NormalizationService()
    return service.run()