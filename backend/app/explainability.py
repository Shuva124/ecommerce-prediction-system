import pickle
import shap
import pandas as pd
from app.config import RAW_XGBOOST_PATH
from app.model_utils import PredictionService

class ExplainabilityService:
    def __init__(self):
        print("Initializing Explainability Service...")
        print(f" -> Loading Raw XGBoost Model for SHAP from: {RAW_XGBOOST_PATH}")
        with open(RAW_XGBOOST_PATH, 'rb') as f:
            self.model = pickle.load(f)
        
        print(" -> Initializing SHAP TreeExplainer...")
        # Initialize Explainer at runtime to avoid pickle versioning bugs
        self.explainer = shap.TreeExplainer(self.model)
        
        # Reuse prediction service to guarantee identical preprocessing
        self.predictor = PredictionService() 

    def explain(self, data_dict: dict, top_n: int = 5) -> dict:
        # 1. Get the actual prediction & probability (from the calibrated model)
        pred_result = self.predictor.predict(data_dict)
        
        # 2. Get the preprocessed dataframe for SHAP (from the raw model)
        X_processed = self.predictor.preprocess(data_dict)
        
        # 3. Calculate SHAP values for this specific session
        shap_values = self.explainer(X_processed)
        
        base_val = float(shap_values.base_values[0])
        val_contributions = shap_values.values[0] if hasattr(shap_values, 'values') else shap_values[0]
        
        # 4. Map impacts to feature names, matching the updated Pydantic schema
        feature_impacts = [
            {"feature": col, "shap_value": float(val_contributions[i])}
            for i, col in enumerate(X_processed.columns)
        ]
        
        # 5. Filter out negligible impacts and sort by absolute magnitude
        feature_impacts = [f for f in feature_impacts if abs(f["shap_value"]) > 0.001]
        feature_impacts.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        
        return {
            "prediction": pred_result["prediction"],
            "purchase_probability": pred_result["purchase_probability"],
            "base_value": round(base_val, 4),
            "feature_impacts": feature_impacts[:top_n]
        }

# Instantiate as a singleton at module level to keep memory overhead low
explain_service = ExplainabilityService()

def explain_purchase(data: dict) -> dict:
    """
    Wrapper function to handle explainability requests.
    Delegates the actual computation to the ExplainabilityService.
    """
    return explain_service.explain(data)