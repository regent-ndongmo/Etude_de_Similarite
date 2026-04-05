"""Chart generation: similarity heatmaps and temporal evolution graphs."""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D


# Colour palette for themes (up to ~10 distinct themes)
_THEME_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
]


# --------------------------------------------------------------------------- #
#  Overall similarity heatmap ordered by clusters                             #
# --------------------------------------------------------------------------- #

def plot_heatmap(df: pd.DataFrame, overall: np.ndarray, outdir: str) -> None:
    """
    Saves heatmap of overall similarity, ordered by cluster.
    Output: <outdir>/heatmap_similarity_clusters.png
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
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Similarity score (0–1)')
    ax.set_title("Overall Similarity Heatmap (ordered by cluster)", fontsize=13, pad=12)

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
    ax.set_xlabel("Study ID")
    ax.set_ylabel("Study ID")

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'heatmap_similarity_clusters.png'), dpi=220)
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Temporal evolution graph                                                   #
# --------------------------------------------------------------------------- #

def plot_temporal_evolution(df: pd.DataFrame, outdir: str) -> None:
    """
    Saves a two-panel chart:
      Panel 1 – Stacked bar chart: publications per year, coloured by theme.
      Panel 2 – Line curve: number of publications per year (NOT cumulative).

    Output: <outdir>/temporal_evolution.png
    """
    df_dated = df.dropna(subset=['year']).copy()
    df_dated['year'] = df_dated['year'].astype(int)

    if df_dated.empty:
        return

    years_range = list(range(df_dated['year'].min(), df_dated['year'].max() + 1))
    themes = sorted(df_dated['theme'].unique())
    color_map = {t: _THEME_COLORS[i % len(_THEME_COLORS)] for i, t in enumerate(themes)}

    # Pivot table: year × theme
    pivot = (
        df_dated.groupby(['year', 'theme'])
        .size()
        .unstack(fill_value=0)
        .reindex(index=years_range, fill_value=0)
    )
    counts_per_year = pivot.sum(axis=1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10), gridspec_kw={'hspace': 0.5})

    # --- Panel 1: stacked bars by theme ---
    bottom = np.zeros(len(pivot))
    for theme in pivot.columns:
        color = color_map.get(theme, '#999999')
        ax1.bar(pivot.index, pivot[theme], bottom=bottom, color=color,
                label=_shorten(theme, 55), width=0.7)
        bottom += pivot[theme].values

    ax1.set_title("Number of Publications per Year by Theme", fontsize=12, pad=10)
    ax1.set_xlabel("Publication year")
    ax1.set_ylabel("Number of studies")
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax1.set_xticks(years_range)
    ax1.set_xticklabels(years_range, rotation=45, ha='right', fontsize=8)

    legend_handles = [
        Line2D([0], [0], color=color_map[t], linewidth=6, label=_shorten(t, 55))
        for t in pivot.columns
    ]
    ax1.legend(
        handles=legend_handles,
        fontsize=7, framealpha=0.85, ncol=1,
        bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0,
    )
    for yr, total in counts_per_year.items():
        if total > 0:
            ax1.text(yr, total + 0.05, str(int(total)),
                     ha='center', va='bottom', fontsize=7, color='#333333')

    # --- Panel 2: line curve — publications per year (not cumulative) ---
    ax2.plot(counts_per_year.index, counts_per_year.values,
             color='#d62728', marker='o', markersize=6, linewidth=2.2,
             label='Publications per year')
    ax2.fill_between(counts_per_year.index, counts_per_year.values,
                     alpha=0.12, color='#d62728')

    ax2.set_title("Annual Number of Publications", fontsize=12, pad=10)
    ax2.set_xlabel("Publication year")
    ax2.set_ylabel("Number of publications")
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax2.set_xticks(years_range)
    ax2.set_xticklabels(years_range, rotation=45, ha='right', fontsize=8)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    ax2.set_ylim(bottom=0)

    # Annotate peak year
    peak_yr = counts_per_year.idxmax()
    peak_val = int(counts_per_year.max())
    ax2.annotate(
        f"Peak: {peak_val} ({peak_yr})",
        xy=(peak_yr, peak_val),
        xytext=(15, 8), textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color='#555555'),
        fontsize=9, color='#d62728',
    )

    fig.savefig(os.path.join(outdir, 'temporal_evolution.png'), dpi=200, bbox_inches='tight')
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Results & Recommendations similarity heatmap                               #
# --------------------------------------------------------------------------- #

def plot_results_heatmap(df: pd.DataFrame, results_sim: np.ndarray, outdir: str) -> None:
    """
    Heatmap of similarity based solely on the Results & Recommendations column.
    Output: <outdir>/heatmap_similarity_results.png
    """
    order = df.sort_values(['cluster_id', 'study_id']).index.to_list()
    ordered = results_sim[np.ix_(order, order)]
    ordered_ids = df.iloc[order]['study_id'].to_list()
    ordered_clusters = df.iloc[order]['cluster_id'].to_list()

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(ordered, aspect='auto', vmin=0, vmax=1, cmap='plasma')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                 label='Results similarity score (0–1)')
    ax.set_title(
        "Results & Recommendations Similarity Heatmap\n"
        "(dedicated vectorisation, ordered by cluster)",
        fontsize=12, pad=12,
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
    ax.set_xlabel("Study ID")
    ax.set_ylabel("Study ID")

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'heatmap_similarity_results.png'), dpi=220)
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Internal helper                                                            #
# --------------------------------------------------------------------------- #

def _shorten(text: str, maxlen: int) -> str:
    return text if len(text) <= maxlen else text[:maxlen - 1] + '…'
