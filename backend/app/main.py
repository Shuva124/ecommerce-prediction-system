import os
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import our strictly typed schemas
from app.schemas import SessionDataInput, PredictionResponse, ExplainResponse

# Import our business logic controllers (Corrected imports)
from app.prediction import predict_purchase
from app.explainability import explain_purchase
from app.config import MODEL_METRICS_PATH, SHAP_TOP_FEATURES_PATH

# Initialize the API
app = FastAPI(
    title="Amazon MLSS - E-Commerce Intent API",
    description="Predicts customer purchase probability and provides real-time SHAP explainability.",
    version="1.0.0"
)

# Configure CORS so our Next.js frontend (running on port 3000) can communicate with us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["System"])
def root():
    """
    Root endpoint for basic API info.
    """
    return {
        "project": "E-Commerce Purchase Prediction",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/health", tags=["System"])
def health_check():
    """
    Simple health check endpoint to verify the server is running.
    """
    return {"status": "ok", "message": "FastAPI is running and ML services are loaded."}

@app.post("/predict", response_model=PredictionResponse, tags=["Machine Learning"])
def predict_intent(payload: SessionDataInput):
    """
    Accepts a single user session and returns the purchase probability and class prediction.
    """
    try:
        return predict_purchase(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/explain", response_model=ExplainResponse, tags=["Machine Learning"])
def explain_intent(payload: SessionDataInput):
    """
    Accepts a single user session and returns the prediction ALONG WITH the real-time SHAP 
    feature impacts explaining exactly *why* the model made that decision.
    """
    try:
        return explain_purchase(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explainability failed: {str(e)}")

@app.get("/metrics", tags=["Dashboard Intelligence"])
def get_metrics():
    """
    Returns the static model comparison metrics (Accuracy, F1, ROC-AUC) generated during training.
    """
    if not os.path.exists(MODEL_METRICS_PATH):
        raise HTTPException(status_code=404, detail="Metrics artifact not found.")
    
    try:
        df = pd.read_csv(MODEL_METRICS_PATH)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load metrics: {str(e)}")

@app.get("/feature-importance", tags=["Dashboard Intelligence"])
def get_feature_importance():
    """
    Returns the top 20 global SHAP feature importances calculated during training.
    """
    if not os.path.exists(SHAP_TOP_FEATURES_PATH):
        raise HTTPException(status_code=404, detail="Feature importance artifact not found.")
    
    try:
        with open(SHAP_TOP_FEATURES_PATH, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load feature importance: {str(e)}")