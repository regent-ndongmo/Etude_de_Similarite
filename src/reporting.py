"""CSV exports, similarity matrix and Markdown report."""

import os
import numpy as np
import pandas as pd
from collections import Counter

from src.utils import shared_keywords, tokenize, FRENCH_STOPWORDS


# --------------------------------------------------------------------------- #
#  Automatic pair interpretation                                              #
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
        drivers.append("résultats/recommandations très similaires")
    elif row['sim_results'] >= 0.12:
        drivers.append("résultats/recommandations similaires")
    if row['sim_text_word'] >= 0.22:
        drivers.append("vocabulaire global très proche")
    elif row['sim_text_word'] >= 0.12:
        drivers.append("vocabulaire global proche")
    if not drivers:
        drivers.append("proximité principalement lexicale")

    score = row['global_score_0_100']
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
#  Main pairs DataFrame                                                       #
# --------------------------------------------------------------------------- #

def build_pairs_dataframe(df: pd.DataFrame, matrices: dict) -> pd.DataFrame:
    """Builds the DataFrame of all pairs (i, j) with i < j."""
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
                'study_id_1':          int(df.at[i, 'study_id']),
                'table_source_1':      int(df.at[i, 'table_index']),
                'row_in_table_1':      int(df.at[i, 'row_index_in_table']),
                'author_1':            df.at[i, 'author'],
                'year_1':              df.at[i, 'year'],
                'country_1':           df.at[i, 'country'],
                'theme_1':             df.at[i, 'theme'],
                'subtheme_1':          df.at[i, 'subtheme'],
                'study_id_2':          int(df.at[j, 'study_id']),
                'table_source_2':      int(df.at[j, 'table_index']),
                'row_in_table_2':      int(df.at[j, 'row_index_in_table']),
                'author_2':            df.at[j, 'author'],
                'year_2':              df.at[j, 'year'],
                'country_2':           df.at[j, 'country'],
                'theme_2':             df.at[j, 'theme'],
                'subtheme_2':          df.at[j, 'subtheme'],
                'global_score_0_1':    round(score, 6),
                'global_score_0_100':  round(score * 100, 2),
                'corpus_percentile':   round(percentile, 2),
                'sim_text_word':       round(float(matrices['word'][i, j]), 6),
                'sim_text_char':       round(float(matrices['char'][i, j]), 6),
                'sim_results':         round(float(matrices['results'][i, j]), 6),
                'sim_method':          round(float(matrices['method'][i, j]), 6),
                'sim_theme':           round(float(matrices['theme'][i, j]), 6),
                'sim_subtheme':        round(float(matrices['subtheme'][i, j]), 6),
                'sim_country':         round(float(matrices['country'][i, j]), 6),
                'shared_keywords':     ', '.join(kw) if kw else '',
            })

    pairs_df = pd.DataFrame(rows).sort_values(
        ['global_score_0_1', 'sim_text_word', 'sim_method'], ascending=False
    ).reset_index(drop=True)

    if not pairs_df.empty:
        pairs_df['interpretation'] = pairs_df.apply(interpret_pair, axis=1)

    return pairs_df


# --------------------------------------------------------------------------- #
#  Nearest neighbour per study                                                #
# --------------------------------------------------------------------------- #

def build_nearest_dataframe(df: pd.DataFrame, overall: np.ndarray) -> pd.DataFrame:
    """Returns the closest neighbour (excluding self) for each study."""
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
            'study_id':             int(df.at[i, 'study_id']),
            'author':               df.at[i, 'author'],
            'year':                 df.at[i, 'year'],
            'country':              df.at[i, 'country'],
            'theme':                df.at[i, 'theme'],
            'subtheme':             df.at[i, 'subtheme'],
            'nearest_study_id':     int(df.at[j, 'study_id']),
            'nearest_author':       df.at[j, 'author'],
            'nearest_year':         df.at[j, 'year'],
            'nearest_country':      df.at[j, 'country'],
            'nearest_theme':        df.at[j, 'theme'],
            'global_score_0_100':   round(float(overall[i, j]) * 100, 2),
            'shared_keywords':      ', '.join(kw),
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
#  Dedicated Results & Recommendations analysis                               #
# --------------------------------------------------------------------------- #

def build_results_analysis(
    df: pd.DataFrame,
    results_sim: np.ndarray,
    top_pairs: int = 50,
    top_neighbours: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Dedicated analysis of the Results & Recommendations column.

    Returns two DataFrames:
      1. results_top_pairs_df  — top-N pairs ranked by results similarity only,
         with shared keywords extracted from the results text.
      2. results_per_study_df  — for each study, its top-K nearest neighbours
         based solely on results similarity, plus a convergence score.
    """
    n = len(df)
    results_texts = df['results_recommendations'].fillna('').tolist()

    # ---- Top pairs ----
    pair_rows = []
    for i in range(n):
        for j in range(i + 1, n):
            s = float(results_sim[i, j])
            kw = shared_keywords(results_texts[i], results_texts[j], limit=6)
            pair_rows.append({
                'study_id_1':          int(df.at[i, 'study_id']),
                'author_1':            df.at[i, 'author'],
                'year_1':              df.at[i, 'year'],
                'theme_1':             df.at[i, 'theme'],
                'study_id_2':          int(df.at[j, 'study_id']),
                'author_2':            df.at[j, 'author'],
                'year_2':              df.at[j, 'year'],
                'theme_2':             df.at[j, 'theme'],
                'same_theme':          df.at[i, 'theme'] == df.at[j, 'theme'],
                'results_similarity':  round(s, 6),
                'results_sim_pct':     round(s * 100, 2),
                'shared_result_keywords': ', '.join(kw) if kw else '',
            })

    results_top_pairs_df = (
        pd.DataFrame(pair_rows)
        .sort_values('results_similarity', ascending=False)
        .head(top_pairs)
        .reset_index(drop=True)
    )

    # ---- Per-study profile ----
    study_rows = []
    for i in range(n):
        sims = results_sim[i].copy()
        sims[i] = -1
        top_idx = np.argsort(sims)[::-1][:top_neighbours]

        # convergence score: mean of top-K neighbours' results similarity
        convergence = round(float(np.mean([results_sim[i, j] for j in top_idx])) * 100, 2)

        # dominant keywords in this study's results text
        toks = Counter(tokenize(results_texts[i]))
        top_kw = [w for w, _ in toks.most_common(8) if w not in FRENCH_STOPWORDS][:5]

        neighbours = '; '.join(
            f"{df.at[int(j), 'author']} ({round(results_sim[i, int(j)] * 100, 1)}%)"
            for j in top_idx
        )

        study_rows.append({
            'study_id':                    int(df.at[i, 'study_id']),
            'author':                      df.at[i, 'author'],
            'year':                        df.at[i, 'year'],
            'theme':                       df.at[i, 'theme'],
            'results_convergence_score':   convergence,
            f'top_{top_neighbours}_similar_results': neighbours,
            'dominant_result_keywords':    ', '.join(top_kw),
        })

    results_per_study_df = (
        pd.DataFrame(study_rows)
        .sort_values('results_convergence_score', ascending=False)
        .reset_index(drop=True)
    )

    return results_top_pairs_df, results_per_study_df


# --------------------------------------------------------------------------- #
#  Save all outputs to disk                                                   #
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
    results_top_pairs_df: pd.DataFrame,
    results_per_study_df: pd.DataFrame,
    overall: np.ndarray,
    result_dir: str,
) -> None:
    """Writes all CSV files into <result_dir>."""
    os.makedirs(result_dir, exist_ok=True)

    df[STUDIES_COLS].to_csv(
        os.path.join(result_dir, 'studies_structured.csv'), index=False)

    pairs_df.to_csv(
        os.path.join(result_dir, 'similarity_pairs_detailed.csv'), index=False)

    pairs_df.head(25).to_csv(
        os.path.join(result_dir, 'top_25_similar_pairs.csv'), index=False)

    nearest_df.to_csv(
        os.path.join(result_dir, 'nearest_neighbour_per_study.csv'), index=False)

    clusters_df.to_csv(
        os.path.join(result_dir, 'study_clusters.csv'), index=False)

    results_top_pairs_df.to_csv(
        os.path.join(result_dir, 'results_recommendations_top_pairs.csv'), index=False)

    results_per_study_df.to_csv(
        os.path.join(result_dir, 'results_recommendations_per_study.csv'), index=False)

    labels_index = [
        f"{sid:02d} - {author}"
        for sid, author in zip(df['study_id'], df['author'])
    ]
    matrix_df = pd.DataFrame(
        np.round(overall * 100, 2),
        index=labels_index,
        columns=labels_index,
    )
    matrix_df.to_csv(os.path.join(result_dir, 'similarity_matrix_0_100.csv'))


# --------------------------------------------------------------------------- #
#  Markdown report                                                            #
# --------------------------------------------------------------------------- #

def write_report(
    df: pd.DataFrame,
    pairs_df: pd.DataFrame,
    clusters_df: pd.DataFrame,
    nearest_df: pd.DataFrame,
    results_top_pairs_df: pd.DataFrame,
    results_per_study_df: pd.DataFrame,
    outdir: str,
) -> None:
    """Génère rapport_interpretation.md dans <outdir> — format pédagogique, accessible à tous."""
    n_studies = len(df)
    n_pairs = len(pairs_df)
    n_clusters = df['cluster_id'].nunique()
    avg_cluster_size = round(n_studies / n_clusters, 2) if n_clusters else 0

    # Quelques statistiques utiles pour enrichir la narration
    top1 = pairs_df.iloc[0]
    top_score = top1['global_score_0_100']
    top_pair = f"{top1['author_1']} et {top1['author_2']}"
    top_kw = top1['shared_keywords']

    # Cluster le plus grand
    biggest_cluster = clusters_df.iloc[0]
    biggest_theme = biggest_cluster['sous_theme_dominant'] or biggest_cluster['theme_dominant']
    biggest_size = int(biggest_cluster['taille_cluster'])

    # Étude la plus convergente sur les résultats
    top_conv = results_per_study_df.iloc[0]
    top_conv_author = top_conv['author']
    top_conv_score = top_conv['results_convergence_score']
    neighbours_key = [k for k in top_conv.index if k.startswith('top_')][0]
    top_conv_neighbours = top_conv[neighbours_key]

    # Distribution des scores
    pct_strong = round((pairs_df['global_score_0_100'] >= 40).mean() * 100, 1)
    pct_moderate = round(((pairs_df['global_score_0_100'] >= 30) & (pairs_df['global_score_0_100'] < 40)).mean() * 100, 1)

    # Années
    years = df['year'].dropna().astype(int)
    year_min, year_max = int(years.min()), int(years.max())
    peak_year = int(df.dropna(subset=['year']).groupby('year').size().idxmax())
    peak_count = int(df.dropna(subset=['year']).groupby('year').size().max())

    L = []

    # =========================================================================
    # PAGE DE TITRE
    # =========================================================================
    L += [
        "# Rapport d'interprétation — Analyse de similarité des études",
        "",
        "> **À qui s'adresse ce rapport ?**  ",
        "> À toute personne souhaitant comprendre les résultats de cette analyse, même sans formation en statistiques ou en informatique.",
        "> Chaque section commence par une explication simple, suivie des données détaillées.",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 1 — QU'EST-CE QUE CETTE ANALYSE ?
    # =========================================================================
    L += [
        "## 1. Qu'est-ce que cette analyse fait exactement ?",
        "",
        "Ce projet a analysé **{} publications scientifiques** portant sur l'éducation en Afrique subsaharienne.".format(n_studies),
        "Pour chaque paire de publications possible (soit **{:,} comparaisons** au total), l'outil a calculé".format(n_pairs),
        "un **score de similarité** : un chiffre entre 0 et 100 qui indique à quel point deux études se ressemblent.",
        "",
        "**Analogie simple :** imaginez deux recettes de cuisine. Si elles utilisent les mêmes ingrédients,",
        "la même technique de cuisson, et donnent un résultat semblable, leur score de similarité sera élevé.",
        "Si l'une est une tarte aux pommes et l'autre un poulet rôti, le score sera proche de zéro.",
        "",
        "Ici, les « ingrédients » comparés sont :",
        "",
        "| Ce qui est comparé | Poids dans le score final | Ce que cela détecte |",
        "|---|---:|---|",
        "| Le texte complet de chaque étude (mots) | 42 % | Études qui parlent des mêmes sujets avec le même vocabulaire |",
        "| Le texte complet (structure des mots) | 10 % | Similarité d'écriture, même si les mots exacts diffèrent |",
        "| La colonne Résultats & Recommandations | 13 % | Études qui arrivent aux mêmes conclusions |",
        "| La méthodologie utilisée | 10 % | Études qui ont utilisé la même approche scientifique |",
        "| Le thème principal | 10 % | Études classées dans la même grande catégorie |",
        "| Le sous-thème | 10 % | Études classées dans la même sous-catégorie précise |",
        "| Le pays ou la zone géographique | 5 % | Études menées dans le même contexte géographique |",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 2 — COMMENT LIRE UN SCORE ?
    # =========================================================================
    L += [
        "## 2. Comment lire un score de similarité ?",
        "",
        "Le score va de **0** (aucun point commun) à **100** (études quasiment identiques).",
        "Dans ce corpus particulier, les scores sont globalement modérés — c'est normal :",
        "les chercheurs ne publient pas deux fois la même étude.",
        "",
        "Voici comment interpréter les valeurs :",
        "",
        "| Score | Ce que cela signifie concrètement | Comment l'expliquer à quelqu'un |",
        "|---|---|---|",
        "| **50 et plus** | Similarité forte — les deux études se ressemblent vraiment beaucoup | « Ces deux études traitent du même sujet, avec la même méthode, et arrivent à des conclusions très proches. » |",
        "| **40 à 49** | Similarité assez forte — beaucoup de points communs importants | « Ces études partagent le même thème central et une approche similaire, même si les contextes diffèrent légèrement. » |",
        "| **30 à 39** | Similarité modérée — des liens solides sur certains aspects | « Ces études abordent des questions voisines ou utilisent des méthodes comparables, mais restent distinctes. » |",
        "| **Moins de 30** | Similarité faible — quelques points communs seulement | « Ces études appartiennent au même domaine général mais traitent de sujets bien différents. » |",
        "",
        f"> **Dans ce corpus :** {pct_strong} % des paires ont un score ≥ 40 (liens forts ou assez forts),",
        f"> et {pct_moderate} % ont un score entre 30 et 40 (liens modérés).",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 3 — VUE D'ENSEMBLE DU CORPUS
    # =========================================================================
    L += [
        "## 3. Vue d'ensemble du corpus",
        "",
        f"- **{n_studies} études** analysées, publiées entre **{year_min}** et **{year_max}**.",
        f"- L'année avec le plus de publications est **{peak_year}** avec **{peak_count} études** parues cette année-là.",
        f"- Les études ont été regroupées en **{n_clusters} familles thématiques** (appelées « clusters »).",
        f"- En moyenne, chaque famille contient **{avg_cluster_size} études**.",
        "",
        "> **Que regarder en premier ?**",
        "> Ouvrez `temporal_evolution.png` pour visualiser comment la production scientifique",
        "> sur ce sujet a évolué au fil des années.",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 4 — LES FAMILLES D'ÉTUDES (CLUSTERS)
    # =========================================================================
    L += [
        "## 4. Les familles d'études (clusters)",
        "",
        "L'analyse a automatiquement regroupé les études qui se ressemblent le plus",
        "en **familles thématiques** appelées « clusters ».",
        "",
        "**Comment comprendre un cluster ?**",
        "C'est comme trier des livres dans une bibliothèque : tous les livres d'un même rayon",
        "partagent un sujet commun. Ici, les études d'un même cluster traitent des mêmes",
        "questions avec des méthodes proches.",
        "",
        f"La famille la plus grande regroupe **{biggest_size} études** autour du thème :",
        f"*« {biggest_theme} »*.",
        "",
        "### Tableau des principales familles d'études",
        "",
        "| # | Taille | Sujet central de la famille | Mots-clés dominants | Exemples d'auteurs |",
        "|---:|:---:|---|---|---|",
    ]
    for i, (_, row) in enumerate(clusters_df.head(10).iterrows(), 1):
        subtheme = row['sous_theme_dominant'] or row['theme_dominant']
        L.append(
            f"| {i} | {int(row['taille_cluster'])} études | {subtheme} "
            f"| {row['mots_cles_dominants']} | {row['exemples_auteurs']} |"
        )
    L += [
        "",
        "> **Comment lire ce tableau ?**",
        "> Chaque ligne est une « famille » d'études. Plus la taille est grande, plus ce sujet",
        "> est représenté dans le corpus. Les mots-clés dominants sont les termes les plus",
        "> fréquents dans toutes les études de cette famille.",
        "",
        "> **Fichier à consulter :** `result/study_clusters.csv` pour la liste complète.",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 5 — LES PAIRES LES PLUS SIMILAIRES
    # =========================================================================
    L += [
        "## 5. Les paires d'études les plus similaires",
        "",
        "Parmi toutes les comparaisons effectuées, voici les paires d'études qui se",
        "ressemblent le plus, toutes dimensions confondues.",
        "",
        f"**La paire la plus similaire du corpus** est :",
        f"> **{top_pair}** — score de **{top_score:.1f}/100**",
        f"> Mots-clés communs : *{top_kw}*",
        "",
        "Cela signifie que ces deux études traitent du même sous-thème, avec une méthode",
        "quasi-identique, et arrivent à des conclusions très proches.",
        "",
        "### Top 20 des paires les plus similaires",
        "",
        "| Rang | Étude 1 | Étude 2 | Thème commun | Score /100 | Ce qui les rapproche |",
        "|---:|---|---|---|---:|---|",
    ]
    for rank, (_, row) in enumerate(pairs_df.head(20).iterrows(), 1):
        e1 = f"{row['author_1']} ({row['country_1']})"
        e2 = f"{row['author_2']} ({row['country_2']})"
        # Extraire l'interprétation courte depuis le champ interpretation
        interp = row.get('interpretation', '')
        # Garder uniquement la partie "facteurs dominants"
        if 'dominant factors:' in interp:
            factors = interp.split('dominant factors:')[-1].strip().rstrip('.')
        else:
            factors = row['shared_keywords']
        L.append(
            f"| {rank} | {e1} | {e2} | {row['theme_1']} "
            f"| **{row['global_score_0_100']:.1f}** | {factors} |"
        )
    L += [
        "",
        "> **Comment lire ce tableau ?**",
        "> - **Rang 1** = la paire la plus similaire du corpus entier.",
        "> - **Score** : plus il est élevé, plus les études se ressemblent (sur 100).",
        "> - **Ce qui les rapproche** : les raisons principales de leur proximité.",
        "",
        "> **Fichier à consulter :** `result/top_25_similar_pairs.csv` (top 25)",
        "> ou `result/similarity_pairs_detailed.csv` (toutes les paires avec tous les détails).",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 6 — ANALYSE DES RÉSULTATS ET RECOMMANDATIONS
    # =========================================================================
    L += [
        "## 6. Analyse dédiée : Résultats et Recommandations",
        "",
        "Cette section est **unique** dans l'analyse : elle compare uniquement la dernière colonne",
        "du document source, celle qui contient les résultats et recommandations de chaque étude.",
        "",
        "**Pourquoi c'est important ?**",
        "Deux études peuvent traiter du même thème mais arriver à des conclusions opposées,",
        "ou inversement, deux études de thèmes différents peuvent aboutir aux mêmes recommandations.",
        "Cette analyse permet de détecter ces convergences que le score global ne montrerait pas.",
        "",
        "**Comment fonctionne le score de convergence ?**",
        "Pour chaque étude, on mesure à quel point ses résultats ressemblent à ceux des autres.",
        "Un score de convergence élevé signifie que plusieurs autres études arrivent aux mêmes conclusions.",
        "",
        f"> **Étude la plus convergente sur ses résultats :** {top_conv_author}",
        f"> avec un score de convergence de **{top_conv_score:.1f}**.",
        f"> Ses voisins les plus proches sur les résultats : {top_conv_neighbours}.",
        "",
        "### 6a. Paires dont les conclusions se ressemblent le plus",
        "",
        "| Rang | Étude 1 | Année | Étude 2 | Année | Même thème ? | Similarité résultats | Mots-clés communs dans les résultats |",
        "|---:|---|---:|---|---:|:---:|---:|---|",
    ]
    for rank, (_, row) in enumerate(results_top_pairs_df.head(15).iterrows(), 1):
        same = "✓ Oui" if row['same_theme'] else "✗ Non"
        yr1 = int(row['year_1']) if pd.notna(row['year_1']) else '—'
        yr2 = int(row['year_2']) if pd.notna(row['year_2']) else '—'
        L.append(
            f"| {rank} | {row['author_1']} | {yr1} "
            f"| {row['author_2']} | {yr2} "
            f"| {same} | **{row['results_sim_pct']:.1f} %** | {row['shared_result_keywords']} |"
        )
    L += [
        "",
        "> **Comment lire ce tableau ?**",
        "> - **Similarité résultats** : pourcentage de ressemblance uniquement sur les conclusions.",
        "> - **Même thème ✓** : les deux études sont classées dans le même thème → convergence attendue.",
        "> - **Même thème ✗** : les deux études viennent de thèmes *différents* mais arrivent à des",
        ">   conclusions similaires → convergence surprenante, à investiguer en priorité.",
        "",
        "### 6b. Les études dont les conclusions convergent le plus (avec d'autres études)",
        "",
        "| Auteur | Année | Score de convergence | Les 3 études aux conclusions les plus proches | Termes dominants dans ses résultats |",
        "|---|---:|---:|---|---|",
    ]
    for _, row in results_per_study_df.head(15).iterrows():
        yr = int(row['year']) if pd.notna(row['year']) else '—'
        neighbours_key = [k for k in row.index if k.startswith('top_')][0]
        L.append(
            f"| {row['author']} | {yr} "
            f"| **{row['results_convergence_score']:.1f}** "
            f"| {row[neighbours_key]} "
            f"| {row['dominant_result_keywords']} |"
        )
    L += [
        "",
        "> **Comment lire ce tableau ?**",
        "> - **Score de convergence** : plus il est élevé, plus les conclusions de cette étude",
        ">   sont partagées par d'autres. Une étude très convergente renforce un consensus scientifique.",
        "> - **Les 3 études les plus proches** : les auteurs dont les résultats ressemblent le plus",
        ">   à ceux de cette étude, avec le pourcentage de similarité entre parenthèses.",
        "> - **Termes dominants** : les mots qui reviennent le plus dans les résultats de cette étude.",
        "",
        "> **Fichiers à consulter :**",
        "> - `result/results_recommendations_top_pairs.csv` — toutes les paires classées par similarité des résultats",
        "> - `result/results_recommendations_per_study.csv` — profil de convergence de chaque étude",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 7 — L'ÉTUDE LA PLUS PROCHE DE CHAQUE PUBLICATION
    # =========================================================================
    L += [
        "## 7. L'étude la plus proche de chaque publication",
        "",
        "Pour chaque étude du corpus, l'analyse a identifié l'étude qui lui ressemble le plus.",
        "C'est le **« voisin le plus proche »**.",
        "",
        "**Utilité pratique :** si vous lisez une étude et voulez trouver rapidement",
        "la publication la plus similaire à citer ou à comparer, cette table vous donne la réponse directement.",
        "",
        "| Étude | Année | Son étude la plus proche | Année | Score /100 | Ce qu'elles ont en commun |",
        "|---|---:|---|---:|---:|---|",
    ]
    for _, row in nearest_df.head(20).iterrows():
        yr = int(row['year']) if pd.notna(row['year']) else '—'
        nyr = int(row['nearest_year']) if pd.notna(row['nearest_year']) else '—'
        L.append(
            f"| {row['author']} | {yr} "
            f"| {row['nearest_author']} | {nyr} "
            f"| **{row['global_score_0_100']:.1f}** | {row['shared_keywords']} |"
        )
    L += [
        "",
        "> **Fichier à consulter :** `result/nearest_neighbour_per_study.csv` pour toutes les études.",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 8 — GUIDE DES VISUALISATIONS
    # =========================================================================
    L += [
        "## 8. Guide de lecture des graphiques",
        "",
        "Trois graphiques ont été générés. Voici comment les lire.",
        "",
        "### `temporal_evolution.png` — Évolution dans le temps",
        "",
        "Ce fichier contient **deux graphiques** superposés :",
        "",
        "**Graphique du haut — Barres empilées :**",
        "- Chaque barre représente une année.",
        "- La hauteur totale = le nombre d'études publiées cette année-là.",
        "- Les couleurs représentent les thèmes : on peut voir quels thèmes dominaient chaque période.",
        f"- Le pic est en **{peak_year}** avec **{peak_count} publications**.",
        "",
        "**Graphique du bas — Courbe annuelle :**",
        "- Montre le nombre brut de publications par an (pas le total cumulé).",
        "- Un pic sur la courbe = une année de forte activité de recherche.",
        "- Un creux = peu de publications cette année-là.",
        "",
        "### `heatmap_similarity_clusters.png` — Carte thermique de similarité globale",
        "",
        "- C'est un tableau de points colorés, où chaque ligne et chaque colonne représente une étude.",
        "- La couleur d'un point indique à quel point les deux études se ressemblent :",
        "  **jaune/clair = très similaires**, **violet/sombre = peu similaires**.",
        "- Les études sont triées par famille : les carrés lumineux sur la diagonale révèlent les clusters.",
        "- Les lignes blanches séparent les différentes familles d'études.",
        "",
        "### `heatmap_similarity_results.png` — Carte thermique des résultats uniquement",
        "",
        "- Identique à la carte précédente, mais **basée uniquement sur les résultats et recommandations**.",
        "- Si deux études sont claires sur cette carte mais sombres sur l'autre :",
        "  → elles ont des **conclusions similaires bien qu'elles traitent de thèmes différents**.",
        "  C'est le signal le plus intéressant à investiguer.",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 9 — GUIDE DES FICHIERS DE DONNÉES
    # =========================================================================
    L += [
        "## 9. À quoi sert chaque fichier de données ?",
        "",
        "| Fichier | Je l'ouvre quand je veux… |",
        "|---|---|",
        "| `studies_structured.csv` | Voir la liste complète des études avec leur famille (cluster) |",
        "| `top_25_similar_pairs.csv` | Identifier rapidement les 25 paires les plus proches |",
        "| `similarity_pairs_detailed.csv` | Fouiller toutes les comparaisons avec tous les scores détaillés |",
        "| `results_recommendations_top_pairs.csv` | Trouver les études qui arrivent aux mêmes conclusions |",
        "| `results_recommendations_per_study.csv` | Savoir quelles études convergent sur leurs résultats |",
        "| `nearest_neighbour_per_study.csv` | Trouver l'étude la plus proche d'une publication donnée |",
        "| `study_clusters.csv` | Voir le résumé de chaque famille thématique |",
        "| `similarity_matrix_0_100.csv` | Consulter le score entre n'importe quelle paire d'études |",
        "",
        "---",
        "",
    ]

    # =========================================================================
    # SECTION 10 — MISES EN GARDE
    # =========================================================================
    L += [
        "## 10. Ce que ces résultats ne disent PAS",
        "",
        "Il est important de comprendre les limites de cette analyse pour ne pas sur-interpréter les scores.",
        "",
        "**1. Un score élevé ne signifie pas que les études se copient.**",
        "Deux études peuvent aborder le même sujet de manière indépendante et rigoureuse.",
        "Un score élevé indique simplement qu'elles sont proches — pas qu'il y a un problème.",
        "",
        "**2. Un score faible ne signifie pas que les études sont sans rapport.**",
        "Si deux études utilisent des vocabulaires très différents pour parler du même phénomène,",
        "l'outil peut sous-estimer leur proximité réelle.",
        "",
        "**3. La similarité des résultats ≠ consensus scientifique.**",
        "Deux études peuvent avoir des résultats textuellement proches mais des conclusions",
        "scientifiques opposées (ex. : l'une conclut à un effet positif, l'autre à un effet négatif).",
        "Le score ne lit pas le sens — il compare les mots.",
        "",
        "**4. Ces scores sont des outils de tri, pas des verdicts.**",
        "Utilisez-les pour orienter votre lecture et repérer les études à comparer,",
        "mais vérifiez toujours qualitativement les paires identifiées comme très proches.",
        "",
        "---",
        "",
        "*Rapport généré automatiquement par le pipeline d'analyse de similarité.*",
    ]

    with open(os.path.join(outdir, 'rapport_interpretation.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
