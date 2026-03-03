from typing import Literal
from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    # --- Identité ---
    age: int = Field(..., ge=18, le=65, examples=[35], description="Âge de l'employé (entre 18 et 65 ans)")
    genre: Literal["M", "F"] = Field(..., examples=["M"], description="M = Homme, F = Femme")
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
    niveau_education: int = Field(..., ge=1, le=5, examples=[3], description="Niveau d'éducation : 1=Lycée, 2=Bac, 3=Licence, 4=Master, 5=Doctorat")
    departement: str = Field(..., examples=["Ventes"])
    niveau_hierarchique_poste: int = Field(..., ge=1, examples=[2], description="Niveau hiérarchique du poste (1 = entrée de gamme, plus élevé = cadre supérieur)")

    # --- Expérience ---
    nombre_experiences_precedentes: int = Field(..., ge=0, examples=[2])
    annee_experience_totale: int = Field(..., ge=0, examples=[10])
    annees_dans_l_entreprise: int = Field(..., ge=0, examples=[5])
    annees_dans_le_poste_actuel: int = Field(..., ge=0, examples=[2])
    annees_sous_responsable_actuel: int = Field(..., ge=0, examples=[3])
    annees_depuis_la_derniere_promotion: int = Field(..., ge=0, examples=[1])

    # --- Performance ---
    note_evaluation_actuelle: int = Field(..., ge=0, le=5, examples=[3], description="Note d'évaluation actuelle (0 = Non évalué, 1 = Faible, ..., 5 = Excellent)")
    note_evaluation_precedente: int = Field(..., ge=0, le=5, examples=[3], description="Note d'évaluation de la période précédente (même échelle)")
    augmentation_salaire_precedente: int = Field(..., ge=0, examples=[15], description="Pourcentage d'augmentation salariale lors de la dernière révision (%)")
    nb_formations_suivies: int = Field(..., ge=0, examples=[2], description="Nombre de formations suivies sur la dernière année")
    nombre_participation_pee: int = Field(..., ge=0, examples=[1], description="Nombre de participations au Plan d'Épargne Entreprise (PEE)")

    # --- Satisfaction ---
    satisfaction_employee_environnement: int = Field(..., ge=0, le=5, examples=[3])
    satisfaction_employee_nature_travail: int = Field(..., ge=0, le=5, examples=[4])
    satisfaction_employee_equipe: int = Field(..., ge=0, le=5, examples=[3])
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=0, le=5, examples=[2])

    # --- Conditions ---
    heure_supplementaires: Literal["Oui", "Non"] = Field(..., examples=["Non"])
    frequence_deplacement: Literal["Aucun", "Occasionnel", "Fréquent"] = Field(..., examples=["Occasionnel"])
    distance_domicile_travail: int = Field(..., ge=0, examples=[10], description="Distance entre le domicile et le lieu de travail (en km)")
    revenu_mensuel: int = Field(..., ge=0, examples=[5000], description="Revenu mensuel brut en euros (€)")


class PredictionOutput(BaseModel):
    model_config = {"json_schema_extra": {"example": {"prediction": 1, "label": "Quitte", "probabilite": 0.7231}}}
    prediction: int = Field(..., description="0 = Reste, 1 = Quitte")
    label: str = Field(..., description="Libellé de la prédiction : 'Reste' ou 'Quitte'")
    probabilite: float = Field(..., description="Probabilité de départ estimée par le modèle (entre 0.0 et 1.0)")
