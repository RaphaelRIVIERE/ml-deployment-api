import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from app.db.session import get_database_url
from app.db.models import Base

engine = create_engine(get_database_url())


def create_database_if_not_exists():
    db_name = os.getenv("DB_NAME")
    default_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/postgres"
    )
    default_engine = create_engine(default_url, isolation_level="AUTOCOMMIT")
    with default_engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name}
        )
        if not result.fetchone():
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Base de données '{db_name}' créée.")
        else:
            print(f"Base de données '{db_name}' déjà existante.")
    default_engine.dispose()


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")


if __name__ == "__main__":
    create_database_if_not_exists()
    create_tables()
