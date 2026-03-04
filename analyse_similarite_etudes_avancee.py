import os, re, unicodedata, zipfile
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from docx import Document
from docx.document import Document as _Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

FRENCH_STOPWORDS = {
    'a','au','aux','avec','ce','ces','dans','de','des','du','elle','en','et','eux','il','ils','je',
    'la','le','les','leur','lui','ma','mais','me','meme','mes','moi','mon','ne','nos','notre','nous',
    'on','ou','par','pas','pour','qu','que','qui','sa','se','ses','son','sur','ta','te','tes','toi','ton',
    'tu','un','une','vos','votre','vous','c','d','l','n','s','y','est','sont','etre','plus','moins',
    'comme','afin','ainsi','cette','cet','leurs','dont','tous','toutes','tout','entre',
    'parmi','si','deux','trois','quatre','cinq','etude','etudier','analyser','examiner','evaluer','aprecier',
    'resultats','recommandations','afrique','subsaharienne','pays','eleves','scolaire','education',
    'primaire','etudes','eleve','ecole','ecoles','impact','analyse','effet','performance','performances',
    'qualite','qualité','reussite','réussite','systeme','systemes','educatif','educatifs'
}

def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("unsupported")
    for child in parent_elm.iterchildren():
        if child.tag.endswith('}p'):
            yield Paragraph(child, parent)
        elif child.tag.endswith('}tbl'):
            yield Table(child, parent)

def normalize_ws(s):
    return re.sub(r'\s+', ' ', (s or '').replace('\xa0',' ')).strip()

def normalize_text(text):
    text = (text or '').replace('\xa0', ' ').lower()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r'[^a-z0-9\s-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    norm = normalize_text(text)
    return [t for t in norm.split() if len(t) >= 3 and t not in FRENCH_STOPWORDS and not t.isdigit()]

def shared_keywords(text_a, text_b, limit=6):
    ta = Counter(tokenize(text_a))
    tb = Counter(tokenize(text_b))
    common = []
    for token in (set(ta) & set(tb)):
        score = ta[token] + tb[token]
        common.append((score, token))
    common.sort(reverse=True)
    return [token for _, token in common[:limit]]

def interpret_pair(row):
    drivers = []
    if row['sim_subtheme'] >= 0.99:
        drivers.append("meme sous-theme")
    elif row['sim_theme'] >= 0.99:
        drivers.append("meme theme")
    if row['sim_method'] >= 0.75:
        drivers.append("methodologie tres proche")
    elif row['sim_method'] >= 0.33:
        drivers.append("methodologie partiellement proche")
    if row['sim_country'] >= 0.99:
        drivers.append("meme contexte geographique")
    elif row['sim_country'] >= 0.5:
        drivers.append("contexte geographique proche")
    if row['sim_text_word'] >= 0.22:
        drivers.append("vocabulaire/resultats tres proches")
    elif row['sim_text_word'] >= 0.12:
        drivers.append("vocabulaire/resultats proches")
    if not drivers:
        drivers.append("proximite principalement lexicale")
    score = row['score_global_0_100']
    if score >= 50:
        level = "similarite forte dans ce corpus"
    elif score >= 40:
        level = "similarite assez forte"
    elif score >= 30:
        level = "similarite moderee"
    else:
        level = "similarite faible a moderee"
    return f"{level}; facteurs dominants: {', '.join(drivers)}."

def extract_studies(input_path):
    doc = Document(input_path)
    themes = []
    last_nonempty_para = None
    for item in iter_block_items(doc):
        if isinstance(item, Paragraph):
            txt = item.text.strip()
            if txt:
                last_nonempty_para = txt
        else:
            row0 = [normalize_ws(c.text) for c in item.rows[0].cells]
            header_candidates = [x for x in row0 if x]
            generic = {
                'numéro','Auteur(s)','Pays ou zone d’étude','Objectif','Données',
                'Méthodologie','Principaux résultats et recommandations de politique éducative'
            }
            theme = None
            if header_candidates and not all(h in generic for h in header_candidates):
                theme = max(header_candidates, key=len)
            if not theme:
                theme = last_nonempty_para or f'Tableau {len(themes)+1}'
            theme = re.sub(r'^Tableau\s*\d+\s*:\s*', '', normalize_ws(theme))
            themes.append(theme)

    records = []
    for ti, table in enumerate(doc.tables):
        theme = themes[ti]
        current_subtheme = ''
        for ri, row in enumerate(table.rows):
            cells = [normalize_ws(c.text) for c in row.cells]
            if len(cells) < 7:
                continue
            author, country, objective, data, methodology, results = cells[1:7]
            if not author:
                continue
            if author in {'Auteur(s)', 'Contextes spécifiques : conflits, mines, multilinguisme'}:
                continue
            if not any([country, objective, data, methodology, results]):
                current_subtheme = author
                continue
            records.append({
                'study_id': len(records) + 1,
                'table_index': ti + 1,
                'row_index_in_table': ri + 1,
                'author': author,
                'country': country,
                'theme': theme,
                'subtheme': current_subtheme if current_subtheme else theme,
                'objective': objective,
                'data': data,
                'methodology': methodology,
                'results_recommendations': results
            })
    return pd.DataFrame(records)

def main(input_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    df = extract_studies(input_path)
    df['text_for_similarity'] = (
        df['theme'].fillna('') + ' ' + df['subtheme'].fillna('') + ' ' +
        df['objective'].fillna('') + ' ' + df['results_recommendations'].fillna('') + ' ' +
        df['methodology'].fillna('')
    )

    word_vectorizer = TfidfVectorizer(
        lowercase=True, strip_accents='unicode', ngram_range=(1, 2),
        min_df=1, stop_words=list(FRENCH_STOPWORDS), sublinear_tf=True
    )
    word_mat = word_vectorizer.fit_transform(df['text_for_similarity'])
    word_sim = cosine_similarity(word_mat)

    char_vectorizer = TfidfVectorizer(
        analyzer='char_wb', ngram_range=(3, 5), min_df=1, sublinear_tf=True
    )
    char_mat = char_vectorizer.fit_transform(df['text_for_similarity'])
    char_sim = cosine_similarity(char_mat)

    n = len(df)
    method_sim = np.zeros((n, n))
    meth_tokens = [set(tokenize(x)) for x in df['methodology']]
    for i in range(n):
        for j in range(i, n):
            a, b = meth_tokens[i], meth_tokens[j]
            s = len(a & b) / len(a | b) if a and b else 0.0
            method_sim[i, j] = method_sim[j, i] = s

    country_sets = [{t for t in tokenize(x) if t not in {'ass', 'zone', 'etude'}} for x in df['country']]
    country_sim = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ci, cj = df.at[i, 'country'], df.at[j, 'country']
            ni, nj = normalize_text(ci), normalize_text(cj)
            if ni and ni == nj:
                s = 1.0
            else:
                si, sj = country_sets[i], country_sets[j]
                s = len(si & sj) / len(si | sj) if si and sj else 0.0
                if 'ass' in ni and 'ass' in nj:
                    s = max(s, 0.6)
            country_sim[i, j] = country_sim[j, i] = s

    theme_vals = df['theme'].astype(str).to_numpy()
    subtheme_vals = df['subtheme'].astype(str).to_numpy()
    theme_sim = (theme_vals[:, None] == theme_vals[None, :]).astype(float)
    subtheme_sim = (subtheme_vals[:, None] == subtheme_vals[None, :]).astype(float)

    overall = (
        0.52 * word_sim +
        0.13 * char_sim +
        0.10 * method_sim +
        0.10 * theme_sim +
        0.10 * subtheme_sim +
        0.05 * country_sim
    )
    np.fill_diagonal(overall, 1.0)

    raw_scores = []
    pair_rows = []
    for i in range(n):
        for j in range(i + 1, n):
            raw_scores.append(float(overall[i, j]))
    raw_scores = np.array(raw_scores)

    for i in range(n):
        for j in range(i + 1, n):
            score = float(overall[i, j])
            percentile = float((raw_scores <= score).mean() * 100)
            kw = shared_keywords(df.at[i, 'text_for_similarity'], df.at[j, 'text_for_similarity'], limit=6)
            pair_rows.append({
                'ligne_etude_1': int(df.at[i, 'study_id']),
                'tableau_source_1': int(df.at[i, 'table_index']),
                'ligne_tableau_1': int(df.at[i, 'row_index_in_table']),
                'auteur_1': df.at[i, 'author'],
                'pays_1': df.at[i, 'country'],
                'theme_1': df.at[i, 'theme'],
                'sous_theme_1': df.at[i, 'subtheme'],
                'ligne_etude_2': int(df.at[j, 'study_id']),
                'tableau_source_2': int(df.at[j, 'table_index']),
                'ligne_tableau_2': int(df.at[j, 'row_index_in_table']),
                'auteur_2': df.at[j, 'author'],
                'pays_2': df.at[j, 'country'],
                'theme_2': df.at[j, 'theme'],
                'sous_theme_2': df.at[j, 'subtheme'],
                'score_global_0_1': round(score, 6),
                'score_global_0_100': round(score * 100, 2),
                'percentile_corpus': round(percentile, 2),
                'sim_text_word': round(float(word_sim[i, j]), 6),
                'sim_text_char': round(float(char_sim[i, j]), 6),
                'sim_method': round(float(method_sim[i, j]), 6),
                'sim_theme': round(float(theme_sim[i, j]), 6),
                'sim_subtheme': round(float(subtheme_sim[i, j]), 6),
                'sim_country': round(float(country_sim[i, j]), 6),
                'mots_cles_communs': ', '.join(kw) if kw else ''
            })
    pairs_df = pd.DataFrame(pair_rows).sort_values(
        ['score_global_0_1', 'sim_text_word', 'sim_method'], ascending=False
    ).reset_index(drop=True)
    if not pairs_df.empty:
        pairs_df['interpretation'] = pairs_df.apply(interpret_pair, axis=1)

    nearest_rows = []
    for i in range(n):
        sims = overall[i].copy()
        sims[i] = -1
        j = int(np.argmax(sims))
        kw = shared_keywords(df.at[i, 'text_for_similarity'], df.at[j, 'text_for_similarity'], limit=5)
        nearest_rows.append({
            'ligne_etude': int(df.at[i, 'study_id']),
            'auteur': df.at[i, 'author'],
            'pays': df.at[i, 'country'],
            'theme': df.at[i, 'theme'],
            'sous_theme': df.at[i, 'subtheme'],
            'voisin_le_plus_proche_ligne': int(df.at[j, 'study_id']),
            'voisin_le_plus_proche_auteur': df.at[j, 'author'],
            'voisin_le_plus_proche_pays': df.at[j, 'country'],
            'voisin_le_plus_proche_theme': df.at[j, 'theme'],
            'score_global_0_100': round(float(overall[i, j]) * 100, 2),
            'mots_cles_communs': ', '.join(kw)
        })
    nearest_df = pd.DataFrame(nearest_rows)

    try:
        model = AgglomerativeClustering(metric='precomputed', linkage='average', distance_threshold=0.74, n_clusters=None)
    except TypeError:
        model = AgglomerativeClustering(affinity='precomputed', linkage='average', distance_threshold=0.74, n_clusters=None)
    labels = model.fit_predict(1 - overall)
    df['cluster_id'] = labels

    cluster_sizes = df.groupby('cluster_id').size().to_dict()
    cluster_label_map = {}
    cluster_keyword_map = {}
    cluster_rows = []
    for cid, grp in df.groupby('cluster_id'):
        theme_mode = grp['theme'].mode().iat[0]
        subtheme_mode = grp['subtheme'].mode().iat[0]
        toks = Counter()
        for txt in grp['text_for_similarity']:
            toks.update(tokenize(txt))
        keywords = [w for w, _ in toks.most_common(12)]
        keywords = [w for w in keywords if w not in {'afrique','subsaharienne','pays','eleves','education','scolaire','primaire'}][:6]
        cluster_keywords = ', '.join(keywords)
        cluster_label = subtheme_mode if subtheme_mode else theme_mode
        cluster_label_map[cid] = cluster_label
        cluster_keyword_map[cid] = cluster_keywords
        cluster_rows.append({
            'cluster_id': int(cid),
            'taille_cluster': int(len(grp)),
            'theme_dominant': theme_mode,
            'sous_theme_dominant': subtheme_mode,
            'mots_cles_dominants': cluster_keywords,
            'exemples_auteurs': '; '.join(grp['author'].head(5))
        })
    clusters_df = pd.DataFrame(cluster_rows).sort_values(['taille_cluster', 'cluster_id'], ascending=[False, True])

    df['taille_cluster'] = df['cluster_id'].map(cluster_sizes)
    df['label_cluster'] = df['cluster_id'].map(cluster_label_map)
    df['mots_cles_cluster'] = df['cluster_id'].map(cluster_keyword_map)

    labels_index = [f"{sid:02d} - {author}" for sid, author in zip(df['study_id'], df['author'])]
    matrix_df = pd.DataFrame(np.round(overall * 100, 2), index=labels_index, columns=labels_index)

    order = (
        df.assign(avg_similarity=np.round(overall.mean(axis=1), 6))
          .sort_values(['cluster_id', 'avg_similarity', 'study_id'], ascending=[True, False, True])
          .index.to_list()
    )
    ordered = overall[np.ix_(order, order)]
    ordered_ids = df.iloc[order]['study_id'].to_list()
    ordered_clusters = df.iloc[order]['cluster_id'].to_list()

    plt.figure(figsize=(12, 10))
    im = plt.imshow(ordered, aspect='auto')
    plt.colorbar(im, fraction=0.046, pad=0.04, label='Similarite (0-1)')
    plt.title("Heatmap de similarite (ordonnee par clusters)")
    step_positions = []
    last = None
    for idx, cid in enumerate(ordered_clusters):
        if last is None:
            last = cid
        elif cid != last:
            step_positions.append(idx - 0.5)
            last = cid
    for pos in step_positions:
        plt.axhline(pos, linewidth=0.5)
        plt.axvline(pos, linewidth=0.5)
    tick_positions = np.arange(0, len(order), max(1, len(order)//15))
    tick_labels = [str(ordered_ids[p]) for p in tick_positions]
    plt.xticks(tick_positions, tick_labels, rotation=90, fontsize=7)
    plt.yticks(tick_positions, tick_labels, fontsize=7)
    plt.xlabel("ID des etudes")
    plt.ylabel("ID des etudes")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, 'heatmap_similarite_clusters.png'), dpi=220)
    plt.close()

    studies_cols = [
        'study_id','table_index','row_index_in_table','author','country','theme','subtheme',
        'objective','data','methodology','results_recommendations','cluster_id','taille_cluster',
        'label_cluster','mots_cles_cluster'
    ]
    base_outdir = outdir
    # Nouveau dossier "result"
    result_dir = os.path.join(base_outdir, "result")

    os.makedirs(result_dir, exist_ok=True)
    df[studies_cols].to_csv(os.path.join(result_dir, 'etudes_extraites_structurees.csv'), index=False)
    pairs_df.to_csv(os.path.join(result_dir, 'paires_similaires_detaillees.csv'), index=False)
    pairs_df.head(25).to_csv(os.path.join(result_dir, 'top_25_paires_similaires.csv'), index=False)
    nearest_df.to_csv(os.path.join(result_dir, 'voisin_le_plus_proche_par_etude.csv'), index=False)
    clusters_df.to_csv(os.path.join(result_dir, 'clusters_etudes.csv'), index=False)
    matrix_df.to_csv(os.path.join(result_dir, 'matrice_similarite_0_100.csv'))
    # Minimal README
    readme = """# Analyse avancee de similarite des etudes

Ouvrez `rapport_interpretation.md` en premier.
Le detail complet est dans `paires_similaires_detaillees.csv`.
"""
    with open(os.path.join(outdir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)

if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'RL New.docx'
    outdir = sys.argv[2] if len(sys.argv) > 2 else 'sortie_analyse'
    main(input_path, outdir)
