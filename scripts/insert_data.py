import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(db_url))
from app.db.models import Employee
from typing import cast, Any


CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dataset.csv")

BOOL_MAP = {"Oui": True, "Non": False}


def insert_employees():
    session = SessionLocal()
    try:
        existing = session.query(Employee).count()
        if existing > 0:
            print(f"Table déjà peuplée ({existing} lignes). Abandon.")
            return

        df = pd.read_csv(CSV_PATH)
        df["a_quitte_l_entreprise"] = df["a_quitte_l_entreprise"].map(BOOL_MAP)

        records = cast(list[dict[str, Any]], df.to_dict(orient="records"))
        session.bulk_insert_mappings(Employee.__mapper__, records)
        session.commit()

        count = session.query(Employee).count()
        print(f"Insertion terminée : {count} employés en base.")

    except Exception as e:
        session.rollback()
        print(f"Erreur : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    insert_employees()
