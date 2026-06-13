from app.model_utils import PredictionService

# Instantiate as a singleton at module level
prediction_service = PredictionService()

def predict_purchase(data: dict) -> dict[str, float | int]:
    """
    Wrapper function to handle prediction requests.
    Delegates the actual computation to the PredictionService.
    """
    return prediction_service.predict(data)