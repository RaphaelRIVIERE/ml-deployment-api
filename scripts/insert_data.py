"""
Insère des employés dans la table `employees` depuis un fichier CSV.
Idempotent : ne fait rien si la table est déjà peuplée.

Usage :
    python scripts/insert_data.py                        # fixtures par défaut
    python scripts/insert_data.py data/dataset.csv       # dataset complet
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import cast, Any

db_url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(db_url))

from app.db.models import Employee

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV = os.path.join(ROOT, "fixtures", "employees.csv")

BOOL_MAP = {"Oui": True, "Non": False}


def insert_employees(csv_path: str = DEFAULT_CSV) -> None:
    session = SessionLocal()
    try:
        existing = session.query(Employee).count()
        if existing > 0:
            print(f"Table déjà peuplée ({existing} lignes). Abandon.")
            return

        df = pd.read_csv(csv_path)
        df["a_quitte_l_entreprise"] = df["a_quitte_l_entreprise"].map(BOOL_MAP)

        records = cast(list[dict[str, Any]], df.to_dict(orient="records"))
        session.bulk_insert_mappings(Employee.__mapper__, records)
        session.commit()

        count = session.query(Employee).count()
        print(f"Insertion terminée : {count} employés en base (source : {csv_path}).")

    except Exception as e:
        session.rollback()
        print(f"Erreur : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    insert_employees(csv_path)
