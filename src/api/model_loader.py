import joblib
import os

def load_trained_model():
    model_path = "models/model_sales_xgboost.joblib"
    features_path = "models/features_list.joblib"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Le modèle est introuvable à l'emplacement : {model_path}")
    
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    
    return model, features
