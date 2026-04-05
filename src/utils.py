"""Utilitaires communs : stopwords, normalisation, tokenisation."""

import re
import unicodedata
from collections import Counter

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


def normalize_ws(s: str) -> str:
    """Normalise les espaces blancs d'une chaîne."""
    return re.sub(r'\s+', ' ', (s or '').replace('\xa0', ' ')).strip()


def normalize_text(text: str) -> str:
    """Minuscule, suppression accents, ponctuation → espace."""
    text = (text or '').replace('\xa0', ' ').lower()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r'[^a-z0-9\s-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text: str) -> list[str]:
    """Tokenise et filtre les stopwords."""
    norm = normalize_text(text)
    return [t for t in norm.split() if len(t) >= 3 and t not in FRENCH_STOPWORDS and not t.isdigit()]


def shared_keywords(text_a: str, text_b: str, limit: int = 6) -> list[str]:
    """Retourne les mots-clés les plus fréquemment partagés entre deux textes."""
    ta = Counter(tokenize(text_a))
    tb = Counter(tokenize(text_b))
    common = sorted(
        [(ta[tok] + tb[tok], tok) for tok in set(ta) & set(tb)],
        reverse=True
    )
    return [tok for _, tok in common[:limit]]
