import os
import sys

# Ajout du dossier src au chemin de recherche pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data.download_data import download_from_s3
from src.data.clean_transform import clean_transform_data
from src.model.train import train_model

def run_full_pipeline():
    # 1. Configuration
    BUCKET_NAME = "s3-g1mg07"
    RAW_TRAIN = "data/train.csv"
    PROCESSED_TRAIN = "data/processed_train.csv"
    MODEL_PATH = "models/model_sales_xgboost.joblib"

    print("--- Démarrage du Pipeline MLOps ---")

    # 2. Téléchargement (S3 -> Local)
    download_from_s3(BUCKET_NAME, "train.csv", RAW_TRAIN)

    # 3. Nettoyage et Transformation
    if os.path.exists(RAW_TRAIN):
        clean_transform_data(RAW_TRAIN, PROCESSED_TRAIN)
    else:
        print("Erreur : Données brutes introuvables.")
        return

    # 4. Entraînement et Sauvegarde
    if os.path.exists(PROCESSED_TRAIN):
        train_model(PROCESSED_TRAIN, MODEL_PATH)
    else:
        print("Erreur : Données transformées introuvables.")
        return

    print("--- Pipeline terminé avec succès ! ---")

if __name__ == "__main__":
    run_full_pipeline()
