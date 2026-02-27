from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import predict
from ml_model.loader import load_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pipeline, app.state.threshold = load_pipeline()
    yield

app = FastAPI(
    title="Futurisys HR Churn API",
    description="API de prédiction du risque de départ des employés",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(predict.router)
