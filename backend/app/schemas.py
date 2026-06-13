from pydantic import BaseModel
from typing import List


class SessionDataInput(BaseModel):
    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: str
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: str
    Weekend: int


class PredictionResponse(BaseModel):
    prediction: int
    purchase_probability: float


class FeatureImpact(BaseModel):
    feature: str
    shap_value: float


class ExplainResponse(BaseModel):
    prediction: int
    purchase_probability: float
    base_value: float
    feature_impacts: List[FeatureImpact]