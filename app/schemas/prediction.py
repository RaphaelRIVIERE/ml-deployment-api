from typing import Literal
from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    # --- Identité ---
    age: int = Field(..., ge=18, le=65, examples=[35])
    genre: int = Field(..., ge=0, le=1, examples=[1], description="0 = Femme, 1 = Homme")
    statut_marital: Literal["Marié(e)", "Célibataire", "Divorcé(e)"] = Field(..., examples=["Marié(e)"])

    # --- Poste ---
    poste: Literal[
        "Cadre Commercial", "Assistant de Direction", "Consultant",
        "Tech Lead", "Manager", "Senior Manager",
        "Représentant Commercial", "Directeur Technique", "Ressources Humaines",
    ] = Field(..., examples=["Consultant"])
    domaine_etude: Literal[
        "Infra & Cloud", "Transformation Digitale", "Marketing",
        "Entrepreunariat", "Autre", "Ressources Humaines",
    ] = Field(..., examples=["Infra & Cloud"])
    niveau_education: int = Field(..., ge=1, le=5, examples=[3])

    # --- Expérience ---
    nombre_experiences_precedentes: int = Field(..., ge=0, examples=[2])
    annee_experience_totale: int = Field(..., ge=0, examples=[10])
    annees_dans_l_entreprise: int = Field(..., ge=0, examples=[5])
    annees_dans_le_poste_actuel: int = Field(..., ge=0, examples=[2])
    annees_sous_responsable_actuel: int = Field(..., ge=0, examples=[3])
    annees_depuis_la_derniere_promotion: int = Field(..., ge=0, examples=[1])

    # --- Performance ---
    note_evaluation_actuelle: int = Field(..., ge=0, le=5, examples=[3])
    note_evaluation_precedente: int = Field(..., ge=0, le=5, examples=[3])
    augmentation_salaire_precedente: int = Field(..., ge=0, examples=[15])
    nb_formations_suivies: int = Field(..., ge=0, examples=[2])
    nombre_participation_pee: int = Field(..., ge=0, examples=[1])

    # --- Satisfaction ---
    satisfaction_employee_environnement: int = Field(..., ge=0, le=5, examples=[3])
    satisfaction_employee_nature_travail: int = Field(..., ge=0, le=5, examples=[4])
    satisfaction_employee_equipe: int = Field(..., ge=0, le=5, examples=[3])
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=0, le=5, examples=[2])

    # --- Conditions ---
    heure_supplementaires: int = Field(..., ge=0, le=1, examples=[0], description="0 = Non, 1 = Oui")
    frequence_deplacement: int = Field(..., ge=0, le=2, examples=[1], description="0 = Aucun, 1 = Occasionnel, 2 = Fréquent")
    distance_domicile_travail: int = Field(..., ge=0, examples=[10])
    revenu_mensuel: int = Field(..., ge=0, examples=[5000])


class PredictionOutput(BaseModel):
    prediction: int = Field(..., description="0 = Reste, 1 = Quitte")
    label: str = Field(..., description="'Reste' ou 'Quitte'")
    probabilite: float = Field(..., description="Probabilité de départ (entre 0 et 1)")
