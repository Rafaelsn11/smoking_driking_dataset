from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
ARTIFACTS = os.path.join(BASE_DIR, "..", "model_artifacts")

try:
    model         = joblib.load(os.path.join(ARTIFACTS, "smoking_model.pkl"))
    scaler        = joblib.load(os.path.join(ARTIFACTS, "scaler.pkl"))
    label_encoder = joblib.load(os.path.join(ARTIFACTS, "label_encoder.pkl"))
    feature_names = joblib.load(os.path.join(ARTIFACTS, "feature_names.pkl"))
except FileNotFoundError as e:
    raise RuntimeError(f"Artefato não encontrado: {e}.")

app = FastAPI(
    title="Smoking Status Predictor",
    description="Prediz o status de tabagismo a partir de indicadores biométricos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schema com os nomes EXATOS das colunas do modelo ─────────────────────────
class PatientData(BaseModel):
    sex: int              = Field(..., ge=0, le=1,   description="Sexo: 0=Feminino, 1=Masculino")
    age: float            = Field(..., gt=0,          description="Idade (anos)")
    waistline: float      = Field(..., gt=0,          description="Circunferência da cintura (cm)")
    SBP: float            = Field(..., gt=0,          description="Pressão sistólica (mmHg)")
    DBP: float            = Field(..., gt=0,          description="Pressão diastólica (mmHg)")
    BLDS: float           = Field(..., gt=0,          description="Glicemia em jejum (mg/dL)")
    tot_chole: float      = Field(..., gt=0,          description="Colesterol total (mg/dL)")
    HDL_chole: float      = Field(..., gt=0,          description="HDL-colesterol (mg/dL)")
    LDL_chole: float      = Field(..., gt=0,          description="LDL-colesterol (mg/dL)")
    triglyceride: float   = Field(..., gt=0,          description="Triglicerídeos (mg/dL)")
    hemoglobin: float     = Field(..., gt=0,          description="Hemoglobina (g/dL)")
    urine_protein: float  = Field(..., gt=0,          description="Proteína na urina (escala 1-6)")
    serum_creatinine: float = Field(..., gt=0,        description="Creatinina sérica (mg/dL)")
    SGOT_AST: float       = Field(..., gt=0,          description="AST/TGO (U/L)")
    SGOT_ALT: float       = Field(..., gt=0,          description="ALT/TGP (U/L)")
    gamma_GTP: float      = Field(..., gt=0,          description="GGT (U/L)")
    DRK_YN: int           = Field(..., ge=0, le=1,   description="Consome álcool: 0=Não, 1=Sim")
    BMI: float            = Field(..., gt=0,          description="IMC (kg/m²)")
    atherogenic_index: float = Field(...,             description="Índice Aterogênico: log10(TG/HDL)")

    class Config:
        json_schema_extra = {
            "example": {
                "sex": 1, "age": 45.0, "waistline": 85.0,
                "SBP": 120.0, "DBP": 80.0, "BLDS": 95.0,
                "tot_chole": 200.0, "HDL_chole": 50.0, "LDL_chole": 120.0,
                "triglyceride": 150.0, "hemoglobin": 14.5,
                "urine_protein": 1.0, "serum_creatinine": 1.0,
                "SGOT_AST": 25.0, "SGOT_ALT": 22.0, "gamma_GTP": 30.0,
                "DRK_YN": 1, "BMI": 24.5, "atherogenic_index": 0.48
            }
        }

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict[str, float]

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Smoking Status Predictor API is running."}

@app.get("/features", tags=["Info"])
def get_features():
    return {"features": feature_names}

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(patient: PatientData):
    try:
        input_df = pd.DataFrame([patient.model_dump()])[feature_names]
        input_scaled = scaler.transform(input_df)
        pred_encoded = model.predict(input_scaled)[0]
        pred_proba   = model.predict_proba(input_scaled)[0]
        pred_label   = label_encoder.inverse_transform([pred_encoded])[0]
        confidence   = float(np.max(pred_proba))
        probabilities = {
            label_encoder.inverse_transform([i])[0]: round(float(p), 4)
            for i, p in enumerate(pred_proba)
        }
        return PredictionResponse(
            prediction=pred_label,
            confidence=round(confidence, 4),
            probabilities=probabilities,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
