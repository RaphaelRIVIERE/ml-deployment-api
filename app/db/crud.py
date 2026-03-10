from sqlalchemy.orm import Session
from app.db.models import Prediction, Log
from app.schemas.prediction import PredictionInput, PredictionOutput


def log_prediction(db: Session, input_data: PredictionInput, output_data: PredictionOutput) -> Prediction:
    record = Prediction(
        **input_data.model_dump(),
        prediction=output_data.prediction,
        probabilite=output_data.probabilite,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_predictions(db: Session, skip: int = 0, limit: int = 100) -> list[Prediction]:
    return (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def log_request(db: Session, endpoint: str, method: str, status_code: int, response_time_ms: float, prediction_id: int | None = None) -> Log:
    record = Log(
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        response_time_ms=response_time_ms,
        prediction_id=prediction_id,
    )
    db.add(record)
    db.commit()
    return record
