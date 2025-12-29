# Sales Forecasting MLOps Project - Groupe G1-MG07

## Description
Cette application est une solution complète de **MLOps** dédiée à la prédiction des ventes. Elle résout le problème de la gestion des stocks en permettant de prévoir la demande pour 50 articles dans 10 magasins différents à l'aide d'un modèle **XGBoost**.

## Technologies utilisées
- **Langage** : Python 3.9
- **Modélisation** : XGBoost, Scikit-learn
- **API** : FastAPI
- **Infrastructure** : Terraform (Infrastructure as Code)
- **Cloud** : AWS (S3, ECR, App Runner, IAM)
- **CI/CD** : GitHub Actions

##  Structure du projet
- `src/data/` : Pipeline ETL (extraction, nettoyage, transformation).
- `src/model/` : Entraînement et sauvegarde du modèle (`.joblib`).
- `src/api/` : Code de l'API FastAPI et logique de prédiction.
- `main.tf` : Déploiement automatisé des ressources AWS.
- `.github/workflows/` : Automatisation des tests et du déploiement.

## Installation et Démarrage local
1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt

2. **Lancer l'API** :
   ```bash
   uvicorn src.api.main:app --reload

4. **Tester** :
   Accédez à http://127.0.0.1:8000/docs.

## Déploiement Cloud
L'API est automatiquement déployée sur AWS App Runner via une image Docker stockée sur Amazon ECR.

Nom de l'app runner : apprunner-g1mg07

URL de l'API : https://8pmqadvq2q.eu-west-3.awsapprunner.com/docs

## Détails du Modèle
- **Algorithme** : XGBoost (Extreme Gradient Boosting).
- **Entraînement** : Le modèle a été entraîné sur le jeu de données "Store Item Demand Forecasting Challenge" (Kaggle), comprenant 5 ans de données de ventes historiques pour 50 articles dans 10 magasins.
- **Preprocessing** : Extraction de caractéristiques temporelles (jour, mois, année, jour de la semaine) pour capturer la saisonnalité.

##  Utilisation de l'API
L'API expose un point de terminaison `POST /predict` qui accepte des données au format JSON.

**Exemple input de requête :**
```json
{
  "date": "2025-12-30",
  "store": 1,
  "item": 1
}
