"""Main entry point for the similarity analysis pipeline."""

import os
import sys

from src.extraction import extract_studies
from src.similarity import compute_all
from src.clustering import fit_clusters, annotate_dataframe, build_cluster_summary
from src.visualization import plot_heatmap, plot_temporal_evolution, plot_results_heatmap
from src.reporting import (
    build_pairs_dataframe,
    build_nearest_dataframe,
    build_results_analysis,
    save_all,
    write_report,
)


def main(input_path: str, outdir: str) -> None:
    result_dir = os.path.join(outdir, 'result')
    os.makedirs(result_dir, exist_ok=True)

    # 1. Extraction
    print("[1/6] Extracting studies from Word document...")
    df = extract_studies(input_path)
    df['text_for_similarity'] = (
        df['theme'].fillna('') + ' '
        + df['subtheme'].fillna('') + ' '
        + df['objective'].fillna('') + ' '
        + df['results_recommendations'].fillna('') + ' '
        + df['methodology'].fillna('')
    )
    print(f"      → {len(df)} studies extracted")

    # 2. Similarity matrices
    print("[2/6] Computing similarity matrices...")
    matrices = compute_all(df)

    # 3. Clustering
    print("[3/6] Agglomerative clustering...")
    labels = fit_clusters(matrices['overall'])
    df = annotate_dataframe(df, labels)
    df = df.reset_index(drop=True)
    clusters_df = build_cluster_summary(df)
    print(f"      → {df['cluster_id'].nunique()} clusters detected")

    # 4. Build result DataFrames
    print("[4/6] Building result tables...")
    pairs_df = build_pairs_dataframe(df, matrices)
    nearest_df = build_nearest_dataframe(df, matrices['overall'])
    results_top_pairs_df, results_per_study_df = build_results_analysis(
        df, matrices['results'], top_pairs=50, top_neighbours=3
    )

    # 5. Charts
    print("[5/6] Generating charts...")
    plot_heatmap(df, matrices['overall'], result_dir)
    plot_temporal_evolution(df, result_dir)
    plot_results_heatmap(df, matrices['results'], result_dir)

    # 6. Save outputs
    print("[6/6] Writing output files...")
    save_all(
        df, pairs_df, nearest_df, clusters_df,
        results_top_pairs_df, results_per_study_df,
        matrices['overall'], result_dir,
    )
    write_report(
        df, pairs_df, clusters_df, nearest_df,
        results_top_pairs_df, results_per_study_df,
        outdir,
    )

    print("\nDone. Output files:")
    print(f"  Charts      : {result_dir}/")
    print(f"    • heatmap_similarity_clusters.png")
    print(f"    • heatmap_similarity_results.png")
    print(f"    • temporal_evolution.png")
    print(f"  Data        : {result_dir}/")
    print(f"    • studies_structured.csv")
    print(f"    • similarity_pairs_detailed.csv")
    print(f"    • top_25_similar_pairs.csv")
    print(f"    • results_recommendations_top_pairs.csv")
    print(f"    • results_recommendations_per_study.csv")
    print(f"    • nearest_neighbour_per_study.csv")
    print(f"    • study_clusters.csv")
    print(f"    • similarity_matrix_0_100.csv")
    print(f"  Report      : {outdir}/rapport_interpretation.md")


if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'RL_New.docx'
    outdir = sys.argv[2] if len(sys.argv) > 2 else 'sortie_analyse'
    main(input_path, outdir)
