from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import field_validator
from pydantic_settings import BaseSettings
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
    app.state.settings = Settings()
    yield

app = FastAPI(
    title="Futurisys HR Churn API",
    description="API de prédiction du risque de départ des employés",
    version="0.7.0",
    lifespan=lifespan,
)

app.include_router(predict.router)
