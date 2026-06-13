import pickle
import pandas as pd
import numpy as np
from app.config import (
    PREPROCESSOR_PATH, 
    CALIBRATED_MODEL_PATH,
    NUMERIC_COLUMNS,
    CATEGORICAL_COLUMNS,
    SKEWED_COLUMNS
)

class PredictionService:
    def __init__(self):
        print("Initializing Prediction Service...")
        print(f" -> Loading Preprocessor from: {PREPROCESSOR_PATH}")
        with open(PREPROCESSOR_PATH, 'rb') as f:
            self.prep = pickle.load(f)
            
        print(f" -> Loading Calibrated Model from: {CALIBRATED_MODEL_PATH}")
        with open(CALIBRATED_MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)

        self.scaler = self.prep['scaler']
        self.feature_cols = self.prep['feature_columns']

    def preprocess(self, data_dict: dict) -> pd.DataFrame:
        df = pd.DataFrame([data_dict])
        
        # 1. Log Transform Skewed Features
        for col in SKEWED_COLUMNS:
            df[col] = np.log1p(df[col])

        # 2. One-Hot Encode Categorical Variables (Strictly mirroring training)
        df = pd.get_dummies(df, columns=CATEGORICAL_COLUMNS, drop_first=True)

        # 3. Matrix Alignment (CRITICAL for production)
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0
        df = df[self.feature_cols]

        # 4. Scale Numerical Features
        df[NUMERIC_COLUMNS] = self.scaler.transform(df[NUMERIC_COLUMNS])
        
        return df

    def predict(self, data_dict: dict) -> dict[str, float | int]:
        X_processed = self.preprocess(data_dict)
        
        # Use predict_proba for accurate percentage representation
        prob = float(self.model.predict_proba(X_processed)[0][1])
        
        # Set threshold
        pred = 1 if prob >= 0.5 else 0
        
        return {
            "prediction": pred,
            "purchase_probability": round(prob, 4)
        }