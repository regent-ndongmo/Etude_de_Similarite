"""Point d'entrée principal de l'analyse de similarité."""

import os
import sys

from src.extraction import extract_studies
from src.similarity import compute_all
from src.clustering import fit_clusters, annotate_dataframe, build_cluster_summary
from src.visualization import plot_heatmap, plot_temporal_evolution, plot_results_heatmap
from src.reporting import (
    build_pairs_dataframe,
    build_nearest_dataframe,
    build_results_similarity_dataframe,
    save_all,
    write_report,
)


def main(input_path: str, outdir: str) -> None:
    result_dir = os.path.join(outdir, 'result')
    os.makedirs(result_dir, exist_ok=True)

    # 1. Extraction
    print("[1/6] Extraction des études depuis le document Word…")
    df = extract_studies(input_path)
    df['text_for_similarity'] = (
        df['theme'].fillna('') + ' '
        + df['subtheme'].fillna('') + ' '
        + df['objective'].fillna('') + ' '
        + df['results_recommendations'].fillna('') + ' '
        + df['methodology'].fillna('')
    )
    print(f"      → {len(df)} études extraites")

    # 2. Similarité
    print("[2/6] Calcul des matrices de similarité…")
    matrices = compute_all(df)

    # 3. Clustering
    print("[3/6] Clustering agglomératif…")
    labels = fit_clusters(matrices['overall'])
    df = annotate_dataframe(df, labels)
    df = df.reset_index(drop=True)  # index propre après annotation
    clusters_df = build_cluster_summary(df)
    print(f"      → {df['cluster_id'].nunique()} clusters détectés")

    # 4. Construction des DataFrames résultats
    print("[4/6] Construction des tableaux de résultats…")
    pairs_df = build_pairs_dataframe(df, matrices)
    nearest_df = build_nearest_dataframe(df, matrices['overall'])
    results_top_df = build_results_similarity_dataframe(df, matrices['results'], top_n=50)

    # 5. Visualisations
    print("[5/6] Génération des graphiques…")
    plot_heatmap(df, matrices['overall'], result_dir)
    plot_temporal_evolution(df, result_dir)
    plot_results_heatmap(df, matrices['results'], result_dir)

    # 6. Exports
    print("[6/6] Écriture des fichiers de sortie…")
    save_all(df, pairs_df, nearest_df, clusters_df, results_top_df,
             matrices['overall'], result_dir)
    write_report(df, pairs_df, clusters_df, nearest_df, outdir)

    print("\nTerminé. Fichiers générés :")
    print(f"  Graphiques  : {result_dir}/")
    print(f"    • heatmap_similarite_clusters.png")
    print(f"    • heatmap_similarite_resultats.png")
    print(f"    • evolution_temporelle.png")
    print(f"  Données     : {result_dir}/")
    print(f"    • etudes_extraites_structurees.csv")
    print(f"    • paires_similaires_detaillees.csv")
    print(f"    • top_25_paires_similaires.csv")
    print(f"    • top_similarite_resultats_recommandations.csv")
    print(f"    • voisin_le_plus_proche_par_etude.csv")
    print(f"    • clusters_etudes.csv")
    print(f"    • matrice_similarite_0_100.csv")
    print(f"  Rapport     : {outdir}/rapport_interpretation.md")


if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'RL_New.docx'
    outdir = sys.argv[2] if len(sys.argv) > 2 else 'sortie_analyse'
    main(input_path, outdir)
