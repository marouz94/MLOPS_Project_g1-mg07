# Utiliser une image Python légère comme base
FROM python:3.9-slim

#  Définir le répertoire de travail dans le conteneur
WORKDIR /app

#  Copier le fichier des dépendances
COPY requirements.txt .

#  Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

#  Copier les dossiers nécessaires au fonctionnement de l'API
COPY src/ /app/src/
COPY models/ /app/models/

#  Exposer le port que FastAPI va utiliser
EXPOSE 8000

#  Commande pour lancer l'API au démarrage du conteneur
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
