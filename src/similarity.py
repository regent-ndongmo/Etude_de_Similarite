"""Calcul de toutes les matrices de similarité."""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils import FRENCH_STOPWORDS, tokenize, normalize_text


def build_text_word_matrix(texts: list[str]) -> np.ndarray:
    """TF-IDF mots (unigrammes + bigrammes) sur le texte complet de chaque étude."""
    vec = TfidfVectorizer(
        lowercase=True, strip_accents='unicode', ngram_range=(1, 2),
        min_df=1, stop_words=list(FRENCH_STOPWORDS), sublinear_tf=True
    )
    mat = vec.fit_transform(texts)
    return cosine_similarity(mat)


def build_text_char_matrix(texts: list[str]) -> np.ndarray:
    """TF-IDF caractères (n-grammes 3-5) sur le texte complet."""
    vec = TfidfVectorizer(
        analyzer='char_wb', ngram_range=(3, 5), min_df=1, sublinear_tf=True
    )
    mat = vec.fit_transform(texts)
    return cosine_similarity(mat)


def build_results_matrix(results: list[str]) -> np.ndarray:
    """
    Vectorisation dédiée de la colonne 'résultats_recommandations'.
    TF-IDF mots (unigrammes + bigrammes) uniquement sur cette colonne.
    """
    vec = TfidfVectorizer(
        lowercase=True, strip_accents='unicode', ngram_range=(1, 2),
        min_df=1, stop_words=list(FRENCH_STOPWORDS), sublinear_tf=True
    )
    mat = vec.fit_transform(results)
    return cosine_similarity(mat)


def build_method_matrix(methodologies: list[str]) -> np.ndarray:
    """Similarité de Jaccard sur les tokens de la colonne méthodologie."""
    n = len(methodologies)
    token_sets = [set(tokenize(m)) for m in methodologies]
    sim = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            a, b = token_sets[i], token_sets[j]
            s = len(a & b) / len(a | b) if a and b else 0.0
            sim[i, j] = sim[j, i] = s
    return sim


def build_country_matrix(countries: list[str]) -> np.ndarray:
    """Similarité géographique : exacte ou Jaccard avec règle ASS."""
    n = len(countries)
    country_sets = [
        {t for t in tokenize(c) if t not in {'ass', 'zone', 'etude'}}
        for c in countries
    ]
    sim = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ni, nj = normalize_text(countries[i]), normalize_text(countries[j])
            if ni and ni == nj:
                s = 1.0
            else:
                si, sj = country_sets[i], country_sets[j]
                s = len(si & sj) / len(si | sj) if si and sj else 0.0
                if 'ass' in ni and 'ass' in nj:
                    s = max(s, 0.6)
            sim[i, j] = sim[j, i] = s
    return sim


def build_theme_subtheme_matrices(
    themes: list[str], subthemes: list[str]
) -> tuple[np.ndarray, np.ndarray]:
    """Matrices binaires d'égalité exacte pour thème et sous-thème."""
    t = np.array(themes)
    s = np.array(subthemes)
    theme_sim = (t[:, None] == t[None, :]).astype(float)
    subtheme_sim = (s[:, None] == s[None, :]).astype(float)
    return theme_sim, subtheme_sim


def build_overall_matrix(
    word_sim: np.ndarray,
    char_sim: np.ndarray,
    results_sim: np.ndarray,
    method_sim: np.ndarray,
    theme_sim: np.ndarray,
    subtheme_sim: np.ndarray,
    country_sim: np.ndarray,
) -> np.ndarray:
    """
    Combine les 7 matrices avec pondération fixe.

    Poids :
      texte global (mots)  : 42 %
      texte global (chars) : 10 %
      résultats dédiés     : 13 %
      méthodologie         : 10 %
      thème                : 10 %
      sous-thème           : 10 %
      pays                 :  5 %
    """
    overall = (
        0.42 * word_sim
        + 0.10 * char_sim
        + 0.13 * results_sim
        + 0.10 * method_sim
        + 0.10 * theme_sim
        + 0.10 * subtheme_sim
        + 0.05 * country_sim
    )
    np.fill_diagonal(overall, 1.0)
    return overall


def compute_all(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """
    Point d'entrée principal : calcule et retourne toutes les matrices.

    Retourne un dict avec les clés :
      word, char, results, method, theme, subtheme, country, overall
    """
    text_full = (
        df['theme'].fillna('') + ' ' + df['subtheme'].fillna('') + ' '
        + df['objective'].fillna('') + ' ' + df['results_recommendations'].fillna('') + ' '
        + df['methodology'].fillna('')
    ).tolist()

    results_texts = df['results_recommendations'].fillna('').tolist()

    word_sim    = build_text_word_matrix(text_full)
    char_sim    = build_text_char_matrix(text_full)
    results_sim = build_results_matrix(results_texts)
    method_sim  = build_method_matrix(df['methodology'].fillna('').tolist())
    country_sim = build_country_matrix(df['country'].fillna('').tolist())
    theme_sim, subtheme_sim = build_theme_subtheme_matrices(
        df['theme'].astype(str).tolist(),
        df['subtheme'].astype(str).tolist(),
    )
    overall = build_overall_matrix(
        word_sim, char_sim, results_sim,
        method_sim, theme_sim, subtheme_sim, country_sim
    )

    return {
        'word': word_sim,
        'char': char_sim,
        'results': results_sim,
        'method': method_sim,
        'theme': theme_sim,
        'subtheme': subtheme_sim,
        'country': country_sim,
        'overall': overall,
    }
