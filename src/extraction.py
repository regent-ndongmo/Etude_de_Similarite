"""Extraction des études depuis un fichier .docx structuré en tableaux thématiques."""

import re
import pandas as pd
from docx import Document
from docx.document import Document as _Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

from src.utils import normalize_ws


def iter_block_items(parent):
    """Itère les paragraphes et tableaux d'un document ou d'une cellule."""
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Type de parent non supporté")
    for child in parent_elm.iterchildren():
        if child.tag.endswith('}p'):
            yield Paragraph(child, parent)
        elif child.tag.endswith('}tbl'):
            yield Table(child, parent)


def extract_year(author: str) -> int | None:
    """Extrait la première année (1900-2099) trouvée dans la chaîne auteur."""
    match = re.search(r'\b((?:19|20)\d{2})\b', author)
    return int(match.group(1)) if match else None


def extract_studies(input_path: str) -> pd.DataFrame:
    """
    Lit le .docx et retourne un DataFrame avec une ligne par étude.

    Colonnes produites :
      study_id, table_index, row_index_in_table,
      author, year, country, theme, subtheme,
      objective, data, methodology, results_recommendations
    """
    doc = Document(input_path)

    # --- détection des thèmes (titre précédant chaque tableau) ---
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
                'numéro', 'Auteur(s)', "Pays ou zone d'étude", 'Objectif', 'Données',
                'Méthodologie', 'Principaux résultats et recommandations de politique éducative'
            }
            theme = None
            if header_candidates and not all(h in generic for h in header_candidates):
                theme = max(header_candidates, key=len)
            if not theme:
                theme = last_nonempty_para or f'Tableau {len(themes) + 1}'
            theme = re.sub(r'^Tableau\s*\d+\s*:\s*', '', normalize_ws(theme))
            themes.append(theme)

    # --- extraction ligne par ligne ---
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
                'year': extract_year(author),
                'country': country,
                'theme': theme,
                'subtheme': current_subtheme if current_subtheme else theme,
                'objective': objective,
                'data': data,
                'methodology': methodology,
                'results_recommendations': results,
            })

    return pd.DataFrame(records)
