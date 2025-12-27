from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from src.api.model_loader import load_trained_model

app = FastAPI(title="Sales Forecasting API")

# Chargement du modèle au démarrage
model, features_list = load_trained_model()

# Définition du format de donnée attendu par l'API
class PredictionInput(BaseModel):
    date: str    # Format "YYYY-MM-DD"
    store: int
    item: int

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de prédiction des ventes "}

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        # 1. Conversion de l'entrée en DataFrame
        input_dict = input_data.dict()
        df = pd.DataFrame([input_dict])
        
        # 2. Feature Engineering (le même que pour l'entraînement)
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['dayofweek'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        
        # 3. Sélection des colonnes dans le bon ordre
        X = df[features_list]
        
        # 4. Prédiction
        prediction = model.predict(X)
        
        return {
            "prediction": float(prediction[0]),
            "unit": "sales",
            "info": input_dict
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
