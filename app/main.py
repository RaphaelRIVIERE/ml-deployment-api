from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import field_validator
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.routes import predict
from ml_model.loader import load_pipeline


class Settings(BaseSettings):
    api_key: str = ""
    db_host: str = ""
    db_port: int = 5432
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""

    model_config = {"env_file": ".env"}


    @field_validator("api_key")
    @classmethod
    def api_key_must_not_be_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("API_KEY doit être défini dans le fichier .env")
        return v


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pipeline, app.state.threshold = load_pipeline()
    settings = Settings()
    app.state.settings = settings
    db_url = (
        f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
    app.state.engine = create_engine(db_url)
    app.state.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=app.state.engine)
    yield
    app.state.engine.dispose()

app = FastAPI(
    title="Futurisys HR Churn API",
    description="API de prédiction du risque de départ des employés",
    version="0.8.0",
    lifespan=lifespan,
)

app.include_router(predict.router)
