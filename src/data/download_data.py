import boto3
import os

def download_from_s3(bucket_name, s3_file_name, local_file_path):
    """
    Télécharge un fichier depuis un bucket S3 vers le stockage local.
    """
    # Création du client S3 (utilise les credentials configurés dans GitHub ou AWS CLI)
    s3 = boto3.client('s3')
    
    try:
        print(f"Téléchargement de {s3_file_name} depuis le bucket {bucket_name}...")
        
        # Création du dossier local s'il n'existe pas
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        
        # Téléchargement
        s3.download_file(bucket_name, s3_file_name, local_file_path)
        print(f"Succès : Fichier sauvegardé sous {local_file_path}")
        
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    # Paramètres à adapter avec tes noms réels
    BUCKET_NAME = "s3-g1mg07"  # Le nom du bucket que tu as créé
    
    # Liste des fichiers à récupérer
    files_to_download = {
        "train.csv": "data/train.csv",
        "test.csv": "data/test.csv"
    }
    
    for s3_name, local_path in files_to_download.items():
        download_from_s3(BUCKET_NAME, s3_name, local_path)
