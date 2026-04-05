"""Génération des visualisations : heatmap de similarité et graphe d'évolution temporelle."""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D


# --------------------------------------------------------------------------- #
#  Heatmap de similarité ordonnée par clusters                                #
# --------------------------------------------------------------------------- #

def plot_heatmap(df: pd.DataFrame, overall: np.ndarray, outdir: str) -> None:
    """
    Génère la heatmap de similarité globale, ordonnée par cluster.
    Sauvegarde dans <outdir>/heatmap_similarite_clusters.png
    """
    order = (
        df.assign(avg_similarity=np.round(overall.mean(axis=1), 6))
          .sort_values(['cluster_id', 'avg_similarity', 'study_id'], ascending=[True, False, True])
          .index.to_list()
    )
    ordered = overall[np.ix_(order, order)]
    ordered_ids = df.iloc[order]['study_id'].to_list()
    ordered_clusters = df.iloc[order]['cluster_id'].to_list()

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(ordered, aspect='auto', vmin=0, vmax=1, cmap='viridis')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Similarité (0–1)')
    ax.set_title("Heatmap de similarité (ordonnée par clusters)", fontsize=13, pad=12)

    # Séparateurs de clusters
    last = None
    for idx, cid in enumerate(ordered_clusters):
        if last is not None and cid != last:
            ax.axhline(idx - 0.5, color='white', linewidth=0.7)
            ax.axvline(idx - 0.5, color='white', linewidth=0.7)
        last = cid

    step = max(1, len(order) // 15)
    tick_pos = np.arange(0, len(order), step)
    tick_lbl = [str(ordered_ids[p]) for p in tick_pos]
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(tick_lbl, rotation=90, fontsize=7)
    ax.set_yticks(tick_pos)
    ax.set_yticklabels(tick_lbl, fontsize=7)
    ax.set_xlabel("ID des études")
    ax.set_ylabel("ID des études")

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'heatmap_similarite_clusters.png'), dpi=220)
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Graphe d'évolution temporelle                                              #
# --------------------------------------------------------------------------- #

# Palette de couleurs pour les thèmes (max ~10 thèmes distincts)
_THEME_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
]


def plot_temporal_evolution(df: pd.DataFrame, outdir: str) -> None:
    """
    Génère deux graphiques d'évolution temporelle dans un seul fichier PNG :

    1. Barres empilées : nombre d'études publiées par année, colorié par thème.
    2. Courbe cumulée : nombre cumulé d'études dans le corpus au fil du temps.

    Sauvegarde dans <outdir>/evolution_temporelle.png
    """
    df_dated = df.dropna(subset=['year']).copy()
    df_dated['year'] = df_dated['year'].astype(int)

    if df_dated.empty:
        return

    years_range = range(df_dated['year'].min(), df_dated['year'].max() + 1)
    themes = sorted(df_dated['theme'].unique())
    color_map = {t: _THEME_COLORS[i % len(_THEME_COLORS)] for i, t in enumerate(themes)}

    # --- tableau pivot : années × thèmes ---
    pivot = (
        df_dated.groupby(['year', 'theme'])
        .size()
        .unstack(fill_value=0)
        .reindex(index=list(years_range), fill_value=0)
    )

    counts_per_year = pivot.sum(axis=1)
    cumulative = counts_per_year.cumsum()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10), gridspec_kw={'hspace': 0.45})

    # --- Graphe 1 : barres empilées ---
    bottom = np.zeros(len(pivot))
    for theme in pivot.columns:
        color = color_map.get(theme, '#999999')
        ax1.bar(pivot.index, pivot[theme], bottom=bottom, color=color,
                label=_shorten(theme, 55), width=0.7)
        bottom += pivot[theme].values

    ax1.set_title("Nombre d'études publiées par année (par thème)", fontsize=12, pad=10)
    ax1.set_xlabel("Année de publication")
    ax1.set_ylabel("Nombre d'études")
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax1.set_xticks(list(years_range))
    ax1.set_xticklabels(list(years_range), rotation=45, ha='right', fontsize=8)

    # Légende compacte hors du graphe
    legend_handles = [
        Line2D([0], [0], color=color_map[t], linewidth=6, label=_shorten(t, 55))
        for t in pivot.columns
    ]
    ax1.legend(
        handles=legend_handles,
        loc='upper left', fontsize=7,
        framealpha=0.85, ncol=1,
        bbox_to_anchor=(1.01, 1), borderaxespad=0
    )

    # Annotation du total par barre
    for yr, total in counts_per_year.items():
        if total > 0:
            ax1.text(yr, total + 0.05, str(int(total)),
                     ha='center', va='bottom', fontsize=7, color='#333333')

    # --- Graphe 2 : courbe cumulée ---
    ax2.plot(cumulative.index, cumulative.values, color='#1f77b4',
             marker='o', markersize=5, linewidth=2, label='Cumul études')
    ax2.fill_between(cumulative.index, cumulative.values, alpha=0.15, color='#1f77b4')

    ax2.set_title("Évolution cumulée du corpus d'études", fontsize=12, pad=10)
    ax2.set_xlabel("Année de publication")
    ax2.set_ylabel("Nombre cumulé d'études")
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax2.set_xticks(list(years_range))
    ax2.set_xticklabels(list(years_range), rotation=45, ha='right', fontsize=8)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)

    # Annotation valeur finale
    last_yr = cumulative.index[-1]
    last_val = int(cumulative.iloc[-1])
    ax2.annotate(
        f"Total : {last_val}",
        xy=(last_yr, last_val),
        xytext=(-30, 10), textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color='#555555'),
        fontsize=9, color='#1f77b4'
    )

    fig.savefig(
        os.path.join(outdir, 'evolution_temporelle.png'),
        dpi=200, bbox_inches='tight'
    )
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Heatmap dédiée : similarité résultats/recommandations                      #
# --------------------------------------------------------------------------- #

def plot_results_heatmap(df: pd.DataFrame, results_sim: np.ndarray, outdir: str) -> None:
    """
    Heatmap de la similarité basée uniquement sur la colonne
    'résultats_recommandations', ordonnée par cluster.
    Sauvegarde dans <outdir>/heatmap_similarite_resultats.png
    """
    order = (
        df.sort_values(['cluster_id', 'study_id'])
          .index.to_list()
    )
    ordered = results_sim[np.ix_(order, order)]
    ordered_ids = df.iloc[order]['study_id'].to_list()
    ordered_clusters = df.iloc[order]['cluster_id'].to_list()

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(ordered, aspect='auto', vmin=0, vmax=1, cmap='plasma')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                 label='Similarité résultats (0–1)')
    ax.set_title(
        "Heatmap de similarité — Résultats & Recommandations\n(vectorisation dédiée, ordonnée par clusters)",
        fontsize=12, pad=12
    )

    last = None
    for idx, cid in enumerate(ordered_clusters):
        if last is not None and cid != last:
            ax.axhline(idx - 0.5, color='white', linewidth=0.7)
            ax.axvline(idx - 0.5, color='white', linewidth=0.7)
        last = cid

    step = max(1, len(order) // 15)
    tick_pos = np.arange(0, len(order), step)
    tick_lbl = [str(ordered_ids[p]) for p in tick_pos]
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(tick_lbl, rotation=90, fontsize=7)
    ax.set_yticks(tick_pos)
    ax.set_yticklabels(tick_lbl, fontsize=7)
    ax.set_xlabel("ID des études")
    ax.set_ylabel("ID des études")

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'heatmap_similarite_resultats.png'), dpi=220)
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Utilitaire interne                                                         #
# --------------------------------------------------------------------------- #

def _shorten(text: str, maxlen: int) -> str:
    return text if len(text) <= maxlen else text[:maxlen - 1] + '…'
