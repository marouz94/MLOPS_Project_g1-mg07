import pandas as pd
import numpy as np
import joblib
import os
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def train_model(data_path, model_output_path):
    # 1. Chargement des données traitées
    df = pd.read_csv(data_path)
    
    # 2. Définition des features (doit correspondre à clean_transform.py)
    FEATURES = ['store', 'item', 'year', 'month', 'day', 'dayofweek', 'quarter']
    TARGET = 'sales'
    
    # 3. Split Temporel (Validation sur les derniers mois)
    # Note: Dans un script de prod, on pourrait utiliser une date dynamique
    split_date = 2017 # Exemple simplifié par année pour le script
    train_df = df[df['year'] < split_date]
    val_df = df[df['year'] >= split_date]
    
    X_train, y_train = train_df[FEATURES], train_df[TARGET]
    X_val, y_val = val_df[FEATURES], val_df[TARGET]
    
    print(f"Entraînement sur {len(X_train)} lignes...")
    
    # 4. Configuration et entraînement du modèle XGBoost
    model = XGBRegressor(
        n_estimators=500, 
        learning_rate=0.05, 
        max_depth=6, 
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # 5. Évaluation rapide
    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    
    print(f"Résultats - MAE: {mae:.4f}, RMSE: {rmse:.4f}")
    
    # 6. Sauvegarde du modèle et des colonnes [cite: 83, 88]
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)
    
    # Sauvegarde de l'ordre des features pour l'API (Fiche 2) [cite: 226]
    joblib.dump(FEATURES, 'models/features_list.joblib')
    
    print(f"Modèle sauvegardé avec succès dans {model_output_path}")

if __name__ == "__main__":
    processed_data = "data/processed_train.csv"
    model_path = "models/model_sales_xgboost.joblib"
    
    if os.path.exists(processed_data):
        train_model(processed_data, model_path)
    else:
        print(f"Erreur : Le fichier {processed_data} est introuvable. Lancez clean_transform.py d'abord.")
