"""Clustering agglomératif sur la matrice de similarité globale."""

import numpy as np
import pandas as pd
from collections import Counter
from sklearn.cluster import AgglomerativeClustering

from src.utils import tokenize

DISTANCE_THRESHOLD = 0.74

# Mots trop génériques à exclure des mots-clés de cluster
_CLUSTER_STOPWORDS = {
    'afrique', 'subsaharienne', 'pays', 'eleves', 'education',
    'scolaire', 'primaire'
}


def fit_clusters(overall: np.ndarray) -> np.ndarray:
    """Applique le clustering agglomératif sur la matrice de distance."""
    try:
        model = AgglomerativeClustering(
            metric='precomputed', linkage='average',
            distance_threshold=DISTANCE_THRESHOLD, n_clusters=None
        )
    except TypeError:
        model = AgglomerativeClustering(
            affinity='precomputed', linkage='average',
            distance_threshold=DISTANCE_THRESHOLD, n_clusters=None
        )
    return model.fit_predict(1 - overall)


def build_cluster_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Construit le tableau récapitulatif des clusters."""
    rows = []
    for cid, grp in df.groupby('cluster_id'):
        theme_mode = grp['theme'].mode().iat[0]
        subtheme_mode = grp['subtheme'].mode().iat[0]
        toks = Counter()
        for txt in grp['text_for_similarity']:
            toks.update(tokenize(txt))
        keywords = [
            w for w, _ in toks.most_common(12)
            if w not in _CLUSTER_STOPWORDS
        ][:6]
        rows.append({
            'cluster_id': int(cid),
            'taille_cluster': int(len(grp)),
            'theme_dominant': theme_mode,
            'sous_theme_dominant': subtheme_mode,
            'mots_cles_dominants': ', '.join(keywords),
            'exemples_auteurs': '; '.join(grp['author'].head(5)),
        })
    return (
        pd.DataFrame(rows)
        .sort_values(['taille_cluster', 'cluster_id'], ascending=[False, True])
        .reset_index(drop=True)
    )


def annotate_dataframe(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """
    Ajoute cluster_id, taille_cluster, label_cluster, mots_cles_cluster au DataFrame.
    Suppose que df contient déjà 'text_for_similarity'.
    """
    df = df.copy()
    df['cluster_id'] = labels

    cluster_sizes = df.groupby('cluster_id').size().to_dict()
    label_map: dict[int, str] = {}
    keyword_map: dict[int, str] = {}

    for cid, grp in df.groupby('cluster_id'):
        theme_mode = grp['theme'].mode().iat[0]
        subtheme_mode = grp['subtheme'].mode().iat[0]
        toks = Counter()
        for txt in grp['text_for_similarity']:
            toks.update(tokenize(txt))
        keywords = [
            w for w, _ in toks.most_common(12)
            if w not in _CLUSTER_STOPWORDS
        ][:6]
        label_map[cid] = subtheme_mode if subtheme_mode else theme_mode
        keyword_map[cid] = ', '.join(keywords)

    df['taille_cluster'] = df['cluster_id'].map(cluster_sizes)
    df['label_cluster'] = df['cluster_id'].map(label_map)
    df['mots_cles_cluster'] = df['cluster_id'].map(keyword_map)
    return df
