from sqlalchemy.orm import Session
from app.db.models import Prediction
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
