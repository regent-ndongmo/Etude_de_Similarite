"""Exports CSV, matrice de similarité et rapport Markdown."""

import os
import numpy as np
import pandas as pd

from src.utils import shared_keywords


# --------------------------------------------------------------------------- #
#  Interprétation automatique d'une paire                                     #
# --------------------------------------------------------------------------- #

def interpret_pair(row: pd.Series) -> str:
    drivers = []
    if row['sim_subtheme'] >= 0.99:
        drivers.append("même sous-thème")
    elif row['sim_theme'] >= 0.99:
        drivers.append("même thème")
    if row['sim_method'] >= 0.75:
        drivers.append("méthodologie très proche")
    elif row['sim_method'] >= 0.33:
        drivers.append("méthodologie partiellement proche")
    if row['sim_country'] >= 0.99:
        drivers.append("même contexte géographique")
    elif row['sim_country'] >= 0.5:
        drivers.append("contexte géographique proche")
    if row['sim_results'] >= 0.25:
        drivers.append("résultats/recommandations très proches")
    elif row['sim_results'] >= 0.12:
        drivers.append("résultats/recommandations proches")
    if row['sim_text_word'] >= 0.22:
        drivers.append("vocabulaire global très proche")
    elif row['sim_text_word'] >= 0.12:
        drivers.append("vocabulaire global proche")
    if not drivers:
        drivers.append("proximité principalement lexicale")

    score = row['score_global_0_100']
    if score >= 50:
        level = "similarité forte dans ce corpus"
    elif score >= 40:
        level = "similarité assez forte"
    elif score >= 30:
        level = "similarité modérée"
    else:
        level = "similarité faible à modérée"
    return f"{level} ; facteurs dominants : {', '.join(drivers)}."


# --------------------------------------------------------------------------- #
#  Construction des DataFrames de résultats                                   #
# --------------------------------------------------------------------------- #

def build_pairs_dataframe(df: pd.DataFrame, matrices: dict) -> pd.DataFrame:
    """Construit le DataFrame de toutes les paires (i, j) avec i < j."""
    overall = matrices['overall']
    n = len(df)

    raw_scores = np.array([
        float(overall[i, j])
        for i in range(n)
        for j in range(i + 1, n)
    ])

    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            score = float(overall[i, j])
            percentile = float((raw_scores <= score).mean() * 100)
            kw = shared_keywords(
                df.at[i, 'text_for_similarity'],
                df.at[j, 'text_for_similarity'],
                limit=6,
            )
            rows.append({
                'ligne_etude_1':       int(df.at[i, 'study_id']),
                'tableau_source_1':    int(df.at[i, 'table_index']),
                'ligne_tableau_1':     int(df.at[i, 'row_index_in_table']),
                'auteur_1':            df.at[i, 'author'],
                'annee_1':             df.at[i, 'year'],
                'pays_1':              df.at[i, 'country'],
                'theme_1':             df.at[i, 'theme'],
                'sous_theme_1':        df.at[i, 'subtheme'],
                'ligne_etude_2':       int(df.at[j, 'study_id']),
                'tableau_source_2':    int(df.at[j, 'table_index']),
                'ligne_tableau_2':     int(df.at[j, 'row_index_in_table']),
                'auteur_2':            df.at[j, 'author'],
                'annee_2':             df.at[j, 'year'],
                'pays_2':              df.at[j, 'country'],
                'theme_2':             df.at[j, 'theme'],
                'sous_theme_2':        df.at[j, 'subtheme'],
                'score_global_0_1':    round(score, 6),
                'score_global_0_100':  round(score * 100, 2),
                'percentile_corpus':   round(percentile, 2),
                'sim_text_word':       round(float(matrices['word'][i, j]), 6),
                'sim_text_char':       round(float(matrices['char'][i, j]), 6),
                'sim_results':         round(float(matrices['results'][i, j]), 6),
                'sim_method':          round(float(matrices['method'][i, j]), 6),
                'sim_theme':           round(float(matrices['theme'][i, j]), 6),
                'sim_subtheme':        round(float(matrices['subtheme'][i, j]), 6),
                'sim_country':         round(float(matrices['country'][i, j]), 6),
                'mots_cles_communs':   ', '.join(kw) if kw else '',
            })

    pairs_df = pd.DataFrame(rows).sort_values(
        ['score_global_0_1', 'sim_text_word', 'sim_method'], ascending=False
    ).reset_index(drop=True)

    if not pairs_df.empty:
        pairs_df['interpretation'] = pairs_df.apply(interpret_pair, axis=1)

    return pairs_df


def build_nearest_dataframe(df: pd.DataFrame, overall: np.ndarray) -> pd.DataFrame:
    """Retourne le voisin le plus proche (hors soi-même) pour chaque étude."""
    n = len(df)
    rows = []
    for i in range(n):
        sims = overall[i].copy()
        sims[i] = -1
        j = int(np.argmax(sims))
        kw = shared_keywords(
            df.at[i, 'text_for_similarity'],
            df.at[j, 'text_for_similarity'],
            limit=5,
        )
        rows.append({
            'ligne_etude':                    int(df.at[i, 'study_id']),
            'auteur':                         df.at[i, 'author'],
            'annee':                          df.at[i, 'year'],
            'pays':                           df.at[i, 'country'],
            'theme':                          df.at[i, 'theme'],
            'sous_theme':                     df.at[i, 'subtheme'],
            'voisin_le_plus_proche_ligne':    int(df.at[j, 'study_id']),
            'voisin_le_plus_proche_auteur':   df.at[j, 'author'],
            'voisin_le_plus_proche_annee':    df.at[j, 'year'],
            'voisin_le_plus_proche_pays':     df.at[j, 'country'],
            'voisin_le_plus_proche_theme':    df.at[j, 'theme'],
            'score_global_0_100':             round(float(overall[i, j]) * 100, 2),
            'mots_cles_communs':              ', '.join(kw),
        })
    return pd.DataFrame(rows)


def build_results_similarity_dataframe(
    df: pd.DataFrame, results_sim: np.ndarray, top_n: int = 50
) -> pd.DataFrame:
    """
    Top-N paires ordonnées par similarité dédiée résultats/recommandations.
    Utile pour identifier des études aux conclusions convergentes
    indépendamment de leur proximité thématique.
    """
    n = len(df)
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            s = float(results_sim[i, j])
            rows.append({
                'auteur_1':      df.at[i, 'author'],
                'annee_1':       df.at[i, 'year'],
                'theme_1':       df.at[i, 'theme'],
                'auteur_2':      df.at[j, 'author'],
                'annee_2':       df.at[j, 'year'],
                'theme_2':       df.at[j, 'theme'],
                'sim_resultats': round(s, 6),
                'sim_resultats_pct': round(s * 100, 2),
            })
    return (
        pd.DataFrame(rows)
        .sort_values('sim_resultats', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


# --------------------------------------------------------------------------- #
#  Exports sur disque                                                          #
# --------------------------------------------------------------------------- #

STUDIES_COLS = [
    'study_id', 'table_index', 'row_index_in_table',
    'author', 'year', 'country', 'theme', 'subtheme',
    'objective', 'data', 'methodology', 'results_recommendations',
    'cluster_id', 'taille_cluster', 'label_cluster', 'mots_cles_cluster',
]


def save_all(
    df: pd.DataFrame,
    pairs_df: pd.DataFrame,
    nearest_df: pd.DataFrame,
    clusters_df: pd.DataFrame,
    results_top_df: pd.DataFrame,
    overall: np.ndarray,
    result_dir: str,
) -> None:
    """Écrit tous les CSV dans <result_dir>."""
    os.makedirs(result_dir, exist_ok=True)

    df[STUDIES_COLS].to_csv(
        os.path.join(result_dir, 'etudes_extraites_structurees.csv'), index=False)

    pairs_df.to_csv(
        os.path.join(result_dir, 'paires_similaires_detaillees.csv'), index=False)

    pairs_df.head(25).to_csv(
        os.path.join(result_dir, 'top_25_paires_similaires.csv'), index=False)

    nearest_df.to_csv(
        os.path.join(result_dir, 'voisin_le_plus_proche_par_etude.csv'), index=False)

    clusters_df.to_csv(
        os.path.join(result_dir, 'clusters_etudes.csv'), index=False)

    results_top_df.to_csv(
        os.path.join(result_dir, 'top_similarite_resultats_recommandations.csv'), index=False)

    labels_index = [
        f"{sid:02d} - {author}"
        for sid, author in zip(df['study_id'], df['author'])
    ]
    matrix_df = pd.DataFrame(
        np.round(overall * 100, 2),
        index=labels_index,
        columns=labels_index,
    )
    matrix_df.to_csv(os.path.join(result_dir, 'matrice_similarite_0_100.csv'))


# --------------------------------------------------------------------------- #
#  Rapport Markdown                                                            #
# --------------------------------------------------------------------------- #

def write_report(
    df: pd.DataFrame,
    pairs_df: pd.DataFrame,
    clusters_df: pd.DataFrame,
    nearest_df: pd.DataFrame,
    outdir: str,
) -> None:
    """Génère rapport_interpretation.md dans <outdir>."""
    n_studies = len(df)
    n_pairs = len(pairs_df)
    n_clusters = df['cluster_id'].nunique()
    avg_cluster_size = round(n_studies / n_clusters, 2) if n_clusters else 0

    lines = [
        "# Rapport d'interprétation — Analyse avancée de similarité\n",
        "## Vue d'ensemble",
        f"- Nombre total d'études extraites : **{n_studies}**",
        f"- Nombre total de paires comparées : **{n_pairs}**",
        f"- Nombre de clusters détectés : **{n_clusters}**",
        f"- Taille moyenne des clusters : **{avg_cluster_size}**\n",
        "## Seuils d'interprétation du score global (/100)",
        "| Seuil | Signification |",
        "|---|---|",
        "| ≥ 50 | Similarité forte dans ce corpus |",
        "| 40 – 49 | Similarité assez forte |",
        "| 30 – 39 | Similarité modérée |",
        "| < 30 | Similarité faible à modérée |\n",
        "## Nouvelles dimensions d'analyse",
        "- **`sim_results`** : similarité dédiée à la colonne *Résultats & Recommandations* (TF-IDF indépendant)",
        "- **`evolution_temporelle.png`** : barres empilées par thème + courbe cumulative",
        "- **`top_similarite_resultats_recommandations.csv`** : top-50 paires les plus proches sur les conclusions\n",
        "## Top 20 des paires les plus similaires",
        "| Rang | Étude 1 | Étude 2 | Thème | Score /100 | %ile | Mots-clés communs |",
        "|---|---|---|---|---:|---:|---|",
    ]

    top20 = pairs_df.head(20)
    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        e1 = f"{row['auteur_1']} ({row['pays_1']})"
        e2 = f"{row['auteur_2']} ({row['pays_2']})"
        lines.append(
            f"| {rank} | {e1} | {e2} | {row['theme_1']} "
            f"| {row['score_global_0_100']:.2f} | {row['percentile_corpus']:.2f} "
            f"| {row['mots_cles_communs']} |"
        )

    lines += [
        "\n## Principaux clusters détectés",
        "| Cluster | Taille | Thème dominant | Sous-thème dominant | Mots-clés | Exemples d'auteurs |",
        "|---:|---:|---|---|---|---|",
    ]
    for _, row in clusters_df.head(10).iterrows():
        lines.append(
            f"| {int(row['cluster_id'])} | {int(row['taille_cluster'])} "
            f"| {row['theme_dominant']} | {row['sous_theme_dominant']} "
            f"| {row['mots_cles_dominants']} | {row['exemples_auteurs']} |"
        )

    lines += [
        "\n## Voisin le plus proche (extrait — 15 premières études)",
        "| ID | Auteur | Année | Voisin le plus proche | Année voisin | Score /100 | Mots-clés |",
        "|---:|---|---:|---|---:|---:|---|",
    ]
    for _, row in nearest_df.head(15).iterrows():
        lines.append(
            f"| {int(row['ligne_etude'])} | {row['auteur']} | {int(row['annee']) if pd.notna(row['annee']) else '—'} "
            f"| {row['voisin_le_plus_proche_auteur']} "
            f"| {int(row['voisin_le_plus_proche_annee']) if pd.notna(row['voisin_le_plus_proche_annee']) else '—'} "
            f"| {row['score_global_0_100']:.2f} | {row['mots_cles_communs']} |"
        )

    lines += [
        "\n## Limites",
        "- Le score mesure une proximité textuelle et structurelle, pas une équivalence scientifique.",
        "- Deux études peuvent être très proches sur la méthode mais diverger sur les conclusions.",
        "- `sim_results` évalue spécifiquement les résultats ; une valeur élevée sans score global élevé "
          "indique des conclusions similaires dans des contextes différents.",
        "- Les scores sont des **outils de tri et de lecture**, à vérifier qualitativement.",
    ]

    with open(os.path.join(outdir, 'rapport_interpretation.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
