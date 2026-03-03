import pandas as pd
import numpy as np


def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["genre"] = df["genre"].str.upper().map({"F": 0, "M": 1})
    df["heure_supplementaires"] = (
        df["heure_supplementaires"].str.capitalize().map({"Non": 0, "Oui": 1})
    )
    df["frequence_deplacement"] = (
        df["frequence_deplacement"].str.capitalize().map({
            "Aucun": 0,
            "Occasionnel": 1,
            "Frequent": 2
        })
    )

    return df


def features_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['stabilite_management'] = df['annees_sous_responsable_actuel'] / (df['annees_dans_le_poste_actuel'] + 1)

    df['flag_surcharge_et_deplacement'] = (
            (df['heure_supplementaires'] == 1) & (df['frequence_deplacement'] == 2)
        ).astype(int)

    df['ratio_promotion_anciennete'] = (
        df['annees_depuis_la_derniere_promotion'] / (df['annees_dans_l_entreprise'] + 1)
    )

    sat_cols = [
        'satisfaction_employee_environnement',
        'satisfaction_employee_nature_travail',
        'satisfaction_employee_equipe',
        'satisfaction_employee_equilibre_pro_perso',
    ]
    df['satisfaction_globale']  = df[sat_cols].sum(axis=1)
    df['satisfaction_min']      = df[sat_cols].min(axis=1)

    df['log_revenu']           = np.log1p(df['revenu_mensuel'])

    return df



def remove_redundant_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop(columns=[
        'niveau_hierarchique_poste',
        'annees_sous_responsable_actuel',
        'annees_depuis_la_derniere_promotion',
        'departement',
        'revenu_mensuel'
    ], errors='ignore')

    return df