# Guide d'execution du projet

Ce guide explique comment relancer l'analyse de similarite sur Linux et Windows, installer les dependances, puis generer les fichiers de sortie.

## 1. Prerequis

- Python 3.10 ou plus recent
- `pip` disponible
- Le fichier source Word `.docx` a analyser (par exemple `RL New.docx`)

Le script principal est :
- `analyse_similarite_etudes_avancee.py`

Le fichier des dependances est :
- `requirements.txt`

## 2. Creer un environnement virtuel

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Si `python3` ne fonctionne pas, essaie :

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l'activation, execute une fois dans le terminal :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

## 3. Installer les dependances

Une fois l'environnement active :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Lancer l'analyse

### Commande generale

```bash
python analyse_similarite_etudes_avancee.py "RL New.docx" sortie_analyse
```

- Le premier argument est le chemin du fichier `.docx`
- Le second argument est le dossier de sortie

### Exemples

#### Linux / macOS

```bash
python analyse_similarite_etudes_avancee.py "RL_New.docx" sortie_analyse
```

#### Windows PowerShell

```powershell
python .\analyse_similarite_etudes_avancee.py ".\RL_New.docx" .\sortie_analyse
```

#### Windows CMD

```bat
python analyse_similarite_etudes_avancee.py "RL New.docx" sortie_analyse
```

## 5. Resultats generes

Le dossier de sortie contiendra notamment :

- `etudes_extraites_structurees.csv` : liste des etudes extraites du document
- `paires_similaires_detaillees.csv` : toutes les paires avec score detaille
- `top_25_paires_similaires.csv` : les 25 paires les plus proches
- `voisin_le_plus_proche_par_etude.csv` : meilleur voisin pour chaque etude
- `clusters_etudes.csv` : regroupements thematiques
- `matrice_similarite_0_100.csv` : matrice complete des scores
- `heatmap_similarite_clusters.png` : visualisation de la similarite

## 6. Comment interpreter rapidement les resultats

### Priorite de lecture

1. Ouvrir `top_25_paires_similaires.csv`
2. Lire `paires_similaires_detaillees.csv` pour les details
3. Utiliser `clusters_etudes.csv` pour voir les groupes thematiques
4. Utiliser `heatmap_similarite_clusters.png` pour une vue d'ensemble

### Colonnes importantes dans `paires_similaires_detaillees.csv`

- `auteur_1`, `auteur_2` : noms des auteurs compares
- `pays_1`, `pays_2` : contexte geographique
- `theme_1`, `theme_2` : theme principal
- `sous_theme_1`, `sous_theme_2` : niveau plus fin de classement
- `ligne_etude_1`, `ligne_etude_2` : identifiants internes des etudes
- `ligne_tableau_1`, `ligne_tableau_2` : ligne d'origine dans le tableau du document
- `score_global_0_100` : score global de similarite sur 100
- `percentile_corpus` : position relative de la paire dans l'ensemble des paires
- `mots_cles_communs` : termes qui rapprochent les deux etudes
- `interpretation` : lecture automatique de la proximite detectee

### Regle pratique pour le score

- `>= 50` : similarite forte dans ce corpus
- `40 a 49.99` : similarite assez forte
- `30 a 39.99` : similarite moderee
- `< 30` : similarite faible a moderee

## 7. Regenerer un fichier de dependances gele

Si tu modifies le projet et veux regenerer un fichier de dependances figees :

```bash
pip freeze > requirements-freeze.txt
```

Attention :
- `requirements.txt` fourni ici contient les dependances principales et leurs versions exactes
- `requirements-freeze.txt` capture tout l'environnement courant (y compris les dependances transitives)

## 8. Desactiver l'environnement virtuel

Quand tu as fini :

```bash
deactivate
```

## 9. Depannage rapide

### Erreur : `python not found`

- Verifier que Python est installe
- Sous Windows, verifier que Python est dans le `PATH`

### Erreur : `No module named ...`

- Verifier que l'environnement virtuel est bien active
- Reinstaller avec :

```bash
pip install -r requirements.txt
```

### Erreur liee au fichier Word

- Verifier que le chemin du `.docx` est correct
- Mettre des guillemets si le nom du fichier contient des espaces

## 10. Commande recommandee pour partager le projet

Pour qu'une autre personne relance le projet facilement, partage au minimum :

- `analyse_similarite_etudes_avancee.py`
- `requirements.txt`
- `README_EXECUTION.md`
- le fichier `.docx` source
