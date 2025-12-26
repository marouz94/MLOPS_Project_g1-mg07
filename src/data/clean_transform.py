import pandas as pd
import numpy as np
import os

def clean_transform_data(input_path, output_path):
    """
    Charge les données brutes, extrait les caractéristiques temporelles
    et sauvegarde les données nettoyées.
    """
    print(f"Chargement des données depuis : {input_path}")
    df = pd.read_csv(input_path)
    
    # Transformation de la date
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    
    # Suppression de la colonne date d'origine pour le modèle
    # (On garde les colonnes numériques extraites)
    df_transformed = df.drop(columns=['date'])
    
    # Création du dossier de sortie si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Sauvegarde au format Parquet ou CSV (Parquet est recommandé en MLOps pour le poids)
    df_transformed.to_csv(output_path, index=False)
    print(f"Données transformées sauvegardées dans : {output_path}")

if __name__ == "__main__":
    # Chemins locaux pour tes tests actuels
    # Plus tard, ces chemins pourront pointer vers S3
    raw_data = "data/train.csv"
    processed_data = "data/processed_train.csv"
    
    if os.path.exists(raw_data):
        clean_transform_data(raw_data, processed_data)
    else:
        print(f"Erreur : Le fichier {raw_data} est introuvable.")
