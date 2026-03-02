import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Prediction
from app.db.crud import log_prediction
from app.schemas.prediction import PredictionInput, PredictionOutput

VALID_INPUT = PredictionInput(
    age=35, genre=1, statut_marital="Marié(e)", poste="Consultant",
    domaine_etude="Infra & Cloud", niveau_education=3,
    nombre_experiences_precedentes=2, annee_experience_totale=10,
    annees_dans_l_entreprise=5, annees_dans_le_poste_actuel=2,
    annees_sous_responsable_actuel=3, annees_depuis_la_derniere_promotion=1,
    note_evaluation_actuelle=3, note_evaluation_precedente=3,
    augmentation_salaire_precedente=15, nb_formations_suivies=2,
    nombre_participation_pee=1, satisfaction_employee_environnement=3,
    satisfaction_employee_nature_travail=4, satisfaction_employee_equipe=3,
    satisfaction_employee_equilibre_pro_perso=2,
    heure_supplementaires=0, frequence_deplacement=1,
    distance_domicile_travail=10, revenu_mensuel=5000,
)
VALID_OUTPUT = PredictionOutput(prediction=0, label="Reste", probabilite=0.30)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_log_prediction_creates_record(db_session):
    record = log_prediction(db_session, VALID_INPUT, VALID_OUTPUT)
    assert record.id is not None
    assert record.prediction == 0
    assert record.probabilite == 0.30


def test_log_prediction_is_retrievable(db_session):
    log_prediction(db_session, VALID_INPUT, VALID_OUTPUT)
    result = db_session.query(Prediction).first()
    assert result is not None
    assert result.age == 35
    assert result.poste == "Consultant"
    assert result.prediction == 0

def test_delete_prediction(db_session):
    record = log_prediction(db_session, VALID_INPUT, VALID_OUTPUT)
    record_id = record.id

    db_session.delete(record)
    db_session.commit()

    result = db_session.get(Prediction, record_id)
    assert result is None

def test_missing_required_field_raises_integrity_error(db_session):
    from sqlalchemy.exc import IntegrityError

    # On crée un Prediction en omettant le champ 'prediction' → NULL interdit
    invalid_record = Prediction(
        **VALID_INPUT.model_dump(),
        probabilite=0.30,
        # prediction= intentionnellement absent → None → violation NOT NULL
    )
    db_session.add(invalid_record)
    with pytest.raises(IntegrityError):
        db_session.commit()
