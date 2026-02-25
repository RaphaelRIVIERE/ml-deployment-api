# Déployez un modèle de Machine Learning

## Description
API de déploiement d'un modèle de Machine Learning développée avec FastAPI.

## Structure du projet
```
mon-projet/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── predict.py
│   ├── schemas/
│   │   └── prediction.py
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   └── crud.py
│
├── ml_model/
│   ├── model.pkl
│   └── loader.py
│
├── scripts/
│   ├── create_db.py
│   └── schema.sql
│
├── tests/
│   ├── test_api.py
│   └── test_model.py
│
├── .github/workflows/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### Prérequis
- Python 3.8+
- PostgreSQL

### Étapes
1. Cloner le repo
```bash
git clone git@github.com:RaphaelRIVIERE/ml-deployment-api.git
cd ton-repo
```

2. Créer et activer le venv
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## Utilisation
*À compléter*

## Déploiement
*À compléter*