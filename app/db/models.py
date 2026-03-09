from sqlalchemy import Column, Integer, SmallInteger, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Identité
    age = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    statut_marital = Column(String, nullable=False)
    revenu_mensuel = Column(Integer, nullable=False)

    # Poste
    departement = Column(String, nullable=False)
    poste = Column(String, nullable=False)
    niveau_hierarchique_poste = Column(SmallInteger, nullable=False)
    domaine_etude = Column(String, nullable=False)
    niveau_education = Column(SmallInteger, nullable=False)

    # Expérience
    nombre_experiences_precedentes = Column(Integer, nullable=False)
    annee_experience_totale = Column(Integer, nullable=False)
    annees_dans_l_entreprise = Column(Integer, nullable=False)
    annees_dans_le_poste_actuel = Column(Integer, nullable=False)
    annees_sous_responsable_actuel = Column(Integer, nullable=False)
    annees_depuis_la_derniere_promotion = Column(Integer, nullable=False)

    # Performance
    note_evaluation_actuelle = Column(SmallInteger, nullable=False)
    note_evaluation_precedente = Column(SmallInteger, nullable=False)
    augmentation_salaire_precedente = Column(Integer, nullable=False)
    nb_formations_suivies = Column(Integer, nullable=False)
    nombre_participation_pee = Column(Integer, nullable=False)

    # Satisfaction
    satisfaction_employee_environnement = Column(SmallInteger, nullable=False)
    satisfaction_employee_nature_travail = Column(SmallInteger, nullable=False)
    satisfaction_employee_equipe = Column(SmallInteger, nullable=False)
    satisfaction_employee_equilibre_pro_perso = Column(SmallInteger, nullable=False)

    # Conditions
    heure_supplementaires = Column(String, nullable=False)
    frequence_deplacement = Column(String, nullable=False)
    distance_domicile_travail = Column(Integer, nullable=False)

    # Cible
    a_quitte_l_entreprise = Column(Boolean, nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Inputs — miroir exact de PredictionInput
    age = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    statut_marital = Column(String, nullable=False)
    poste = Column(String, nullable=False)
    domaine_etude = Column(String, nullable=False)
    niveau_education = Column(SmallInteger, nullable=False)
    departement = Column(String, nullable=False)
    niveau_hierarchique_poste = Column(SmallInteger, nullable=False)
    nombre_experiences_precedentes = Column(Integer, nullable=False)
    annee_experience_totale = Column(Integer, nullable=False)
    annees_dans_l_entreprise = Column(Integer, nullable=False)
    annees_dans_le_poste_actuel = Column(Integer, nullable=False)
    annees_sous_responsable_actuel = Column(Integer, nullable=False)
    annees_depuis_la_derniere_promotion = Column(Integer, nullable=False)
    note_evaluation_actuelle = Column(SmallInteger, nullable=False)
    note_evaluation_precedente = Column(SmallInteger, nullable=False)
    augmentation_salaire_precedente = Column(Integer, nullable=False)
    nb_formations_suivies = Column(Integer, nullable=False)
    nombre_participation_pee = Column(Integer, nullable=False)
    satisfaction_employee_environnement = Column(SmallInteger, nullable=False)
    satisfaction_employee_nature_travail = Column(SmallInteger, nullable=False)
    satisfaction_employee_equipe = Column(SmallInteger, nullable=False)
    satisfaction_employee_equilibre_pro_perso = Column(SmallInteger, nullable=False)
    heure_supplementaires = Column(String, nullable=False)
    frequence_deplacement = Column(String, nullable=False)
    distance_domicile_travail = Column(Integer, nullable=False)
    revenu_mensuel = Column(Integer, nullable=False)

    # Outputs
    prediction = Column(SmallInteger, nullable=False)
    probabilite = Column(Float, nullable=False)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=True)