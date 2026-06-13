import os

# backend/
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Directories
MODELS_DIR = os.path.join(BASE_DIR, "models")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

# Models
PREPROCESSOR_PATH = os.path.join(
    MODELS_DIR,
    "preprocessor.pkl"
)

CALIBRATED_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "calibrated_best_model.pkl"
)

RAW_XGBOOST_PATH = os.path.join(
    MODELS_DIR,
    "xgboost.pkl"
)

# Artifacts
MODEL_METRICS_PATH = os.path.join(
    ARTIFACTS_DIR,
    "model_metrics.csv"
)

FEATURE_IMPORTANCE_PATH = os.path.join(
    ARTIFACTS_DIR,
    "feature_importance.csv"
)

SHAP_TOP_FEATURES_PATH = os.path.join(
    ARTIFACTS_DIR,
    "shap_top_features.json"
)