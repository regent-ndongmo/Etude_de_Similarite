# Rapport d'interprétation — Analyse de similarité des études

> **À qui s'adresse ce rapport ?**  
> À toute personne souhaitant comprendre les résultats de cette analyse, même sans formation en statistiques ou en informatique.
> Chaque section commence par une explication simple, suivie des données détaillées.

---

## 1. Qu'est-ce que cette analyse fait exactement ?

Ce projet a analysé **82 publications scientifiques** portant sur l'éducation en Afrique subsaharienne.
Pour chaque paire de publications possible (soit **3,321 comparaisons** au total), l'outil a calculé
un **score de similarité** : un chiffre entre 0 et 100 qui indique à quel point deux études se ressemblent.

**Analogie simple :** imaginez deux recettes de cuisine. Si elles utilisent les mêmes ingrédients,
la même technique de cuisson, et donnent un résultat semblable, leur score de similarité sera élevé.
Si l'une est une tarte aux pommes et l'autre un poulet rôti, le score sera proche de zéro.

Ici, les « ingrédients » comparés sont :

| Ce qui est comparé | Poids dans le score final | Ce que cela détecte |
|---|---:|---|
| Le texte complet de chaque étude (mots) | 42 % | Études qui parlent des mêmes sujets avec le même vocabulaire |
| Le texte complet (structure des mots) | 10 % | Similarité d'écriture, même si les mots exacts diffèrent |
| La colonne Résultats & Recommandations | 13 % | Études qui arrivent aux mêmes conclusions |
| La méthodologie utilisée | 10 % | Études qui ont utilisé la même approche scientifique |
| Le thème principal | 10 % | Études classées dans la même grande catégorie |
| Le sous-thème | 10 % | Études classées dans la même sous-catégorie précise |
| Le pays ou la zone géographique | 5 % | Études menées dans le même contexte géographique |

---

## 2. Comment lire un score de similarité ?

Le score va de **0** (aucun point commun) à **100** (études quasiment identiques).
Dans ce corpus particulier, les scores sont globalement modérés — c'est normal :
les chercheurs ne publient pas deux fois la même étude.

Voici comment interpréter les valeurs :

| Score | Ce que cela signifie concrètement | Comment l'expliquer à quelqu'un |
|---|---|---|
| **50 et plus** | Similarité forte — les deux études se ressemblent vraiment beaucoup | « Ces deux études traitent du même sujet, avec la même méthode, et arrivent à des conclusions très proches. » |
| **40 à 49** | Similarité assez forte — beaucoup de points communs importants | « Ces études partagent le même thème central et une approche similaire, même si les contextes diffèrent légèrement. » |
| **30 à 39** | Similarité modérée — des liens solides sur certains aspects | « Ces études abordent des questions voisines ou utilisent des méthodes comparables, mais restent distinctes. » |
| **Moins de 30** | Similarité faible — quelques points communs seulement | « Ces études appartiennent au même domaine général mais traitent de sujets bien différents. » |

> **Dans ce corpus :** 0.2 % des paires ont un score ≥ 40 (liens forts ou assez forts),
> et 3.6 % ont un score entre 30 et 40 (liens modérés).

---

## 3. Vue d'ensemble du corpus

- **82 études** analysées, publiées entre **2001** et **2025**.
- L'année avec le plus de publications est **2022** avec **13 études** parues cette année-là.
- Les études ont été regroupées en **21 familles thématiques** (appelées « clusters »).
- En moyenne, chaque famille contient **3.9 études**.

> **Que regarder en premier ?**
> Ouvrez `temporal_evolution.png` pour visualiser comment la production scientifique
> sur ce sujet a évolué au fil des années.

---

## 4. Les familles d'études (clusters)

L'analyse a automatiquement regroupé les études qui se ressemblent le plus
en **familles thématiques** appelées « clusters ».

**Comment comprendre un cluster ?**
C'est comme trier des livres dans une bibliothèque : tous les livres d'un même rayon
partagent un sujet commun. Ici, les études d'un même cluster traitent des mêmes
questions avec des méthodes proches.

La famille la plus grande regroupe **19 études** autour du thème :
*« Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage »*.

### Tableau des principales familles d'études

| # | Taille | Sujet central de la famille | Mots-clés dominants | Exemples d'auteurs |
|---:|:---:|---|---|---|
| 1 | 19 études | Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage | apprentissage, inegalites, determinants, lecture, specifiques, facteurs | Spaul (2011); Yu et Thomas (2008); Hungi et Thuku (2009); Taniguchi (2022); Smith et Barrett (2010) |
| 2 | 13 études | Facteurs socio-économiques et inégalités et participation communautaire | facteurs, socio-economiques, participation, communautaire, inegalites, scolaires | Dickerson et al., (2015); Kyei (2021); Miningou (2022); Zuze et Reddy (2014); Barnett (2013) |
| 3 | 11 études | Principaux résultats et recommandations de politique éducative | enseignants, principaux, politique, educative, formation, ameliorer | Wamala et Seruwagi (2012); Lee et al., (2018); Armstrong (2015); Conto et al., (2023); Sanfo (2020) |
| 4 | 6 études | Mesure de la qualité de l’éducation et analyse comparative | comparative, contextes, specifiques, conflits, mines, multilinguisme | Mioko et Cappelle (2015); Spaull et Taylor (2015); Murimba (2005); Dolata (2008); Sandefur (2017) |
| 5 | 4 études | Efficience et efficacité des systèmes éducatifs | efficience, efficacite, ressources, apprentissage, politiques, etablissements | Miningou et al., (2019); Avom et al., (2021); Figueiredo et Dieng (2016); Kouamo (2024) |
| 6 | 4 études | Ressources pédagogiques et infrastructures | ressources, manuels, acces, contextes, specifiques, pedagogiques | Kuecken et al., (2013); Frölich et Michaelowa (2011); Zuze et Leibbrandt (2010); Fehrler et al., (2009) |
| 7 | 3 études | Politiques éducatives et réformes | apc, competences, politiques, ressources, contextes, specifiques | Kadio et al., (2022); Hanchane et Kadio (2022); Atuhurra (2016) |
| 8 | 3 études | Contextes spécifiques : conflits, mines, multilinguisme | conflits, contextes, specifiques, mines, multilinguisme, mathematiques | Sanfo (2021); Garrouste (2011); Salah et Saxena (2025) |
| 9 | 3 études | Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage | cours, apprentissage, supplementaires, inegalites, particuliers, incidence | Bennell (2023); Paviot et al., (2008); Crouch et al. (2021) |
| 10 | 3 études | Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage | mathematiques, francophones, determinants, inegalites, apprentissage, cameroun | Armand et al., (2024); Medu et Rowlands (2022); Bekkouche et Dupraz (2023) |

> **Comment lire ce tableau ?**
> Chaque ligne est une « famille » d'études. Plus la taille est grande, plus ce sujet
> est représenté dans le corpus. Les mots-clés dominants sont les termes les plus
> fréquents dans toutes les études de cette famille.

> **Fichier à consulter :** `result/study_clusters.csv` pour la liste complète.

---

## 5. Les paires d'études les plus similaires

Parmi toutes les comparaisons effectuées, voici les paires d'études qui se
ressemblent le plus, toutes dimensions confondues.

**La paire la plus similaire du corpus** est :
> **Nguemkap et Dieng (2022) et Ongo et al., (2022)** — score de **51.7/100**
> Mots-clés communs : *mathematiques, lecture, scolaires, specifiques, niveau, famille*

Cela signifie que ces deux études traitent du même sous-thème, avec une méthode
quasi-identique, et arrivent à des conclusions très proches.

### Top 20 des paires les plus similaires

| Rang | Étude 1 | Étude 2 | Thème commun | Score /100 | Ce qui les rapproche |
|---:|---|---|---|---:|---|
| 1 | Nguemkap et Dieng (2022) (Cameroun) | Ongo et al., (2022) (ASS, 14 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **51.7** | mathematiques, lecture, scolaires, specifiques, niveau, famille |
| 2 | Sumida et Kawata (2021) (ASS, 15 pays) | Burger (2011) (Zambie) | Facteurs socio-économiques et inégalités et participation communautaire | **46.9** | zones, rurales, differences, ressources, ecart, socio-economiques |
| 3 | Taniguchi (2022) (ASS, 15 pays) | Taniguchi (2024) (ASS, 15 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **44.0** | enfants, ressources, meilleurs, defavorises, ceux, apprentissage |
| 4 | Miningou (2022) (ASS 10 pays) | Sumida et Kawata (2021) (ASS, 15 pays) | Facteurs socio-économiques et inégalités et participation communautaire | **43.0** | ecart, apprentissage, socio-economiques, participation, inegalites, facteurs |
| 5 | Kazima et al., (2022) (Malawi) | Kazima (2014) (Botswana, Malawi et Zambie) | Contextes spécifiques : conflits, mines, multilinguisme | **41.5** | mathematiques, enseignement, reformes, enseignants, malawi, ameliorer |
| 6 | Miningou (2022) (ASS 10 pays) | Burger (2011) (Zambie) | Facteurs socio-économiques et inégalités et participation communautaire | **40.0** | ecart, ressources, socio-economiques, participation, inegalites, facteurs |
| 7 | Ongo et al., (2022) (ASS, 14 pays) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **39.6** | scolaires, inegalites, specifiques, sein, differences, determinants |
| 8 | Smith et Barrett (2010) (ASS, 6 pays) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **39.4** | apprentissage, ressources, inegalites, specifiques, politiques, determinants |
| 9 | Mioko et Cappelle (2015) (ASS, 11 pays) | Murimba (2005) (ASS, 15 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **39.2** | recherche, politiques, statistique, specifiques, multilinguisme, mines |
| 10 | Armstrong (2015) (ASS, 15 pays) | Kanyongo et Brown (2013) (Namibie) | Principaux résultats et recommandations de politique éducative | **38.7** | enseignants, mathematiques, principaux, politique, educative, ages |
| 11 | Zhang (2006) (ASS, 14 pays) | Sumida et Kawata (2021) (ASS, 15 pays) | Facteurs socio-économiques et inégalités et participation communautaire | **38.1** | rurales, zones, apprentissage, facteurs, differences, urbaines |
| 12 | Smith et Barrett (2010) (ASS, 6 pays) | Ongo et al., (2022) (ASS, 14 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **38.0** | lecture, apprentissage, scolaires, specifiques, opportunites, niveaux |
| 13 | Nguemkap et Dieng (2022) (Cameroun) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **37.8** | niveau, inegalites, determinants, specifiques, socio-economique, sein |
| 14 | Hungi et Thuku (2009) (Kenya) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **37.5** | inegalites, socio-economique, determinants, apprentissage, specifiques, sociale |
| 15 | Sanfo (2020) (Burkina Faso) | Foueka et Elomo (2022) (ASS, 10 pays) | Principaux résultats et recommandations de politique éducative | **37.4** | formation, principaux, politique, educative, niveaux, modele |
| 16 | Lee et al., (2005) (ASS, 14 pays) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **37.0** | inegalites, ressources, determinants, apprentissage, specifiques, opportunites |
| 17 | Miningou et al., (2019) (ASS 10 pays) | Avom et al., (2021) (ASS, 10 pays) | Efficience et efficacité des systèmes éducatifs | **36.7** | efficience, efficacite, ressources, politiques, primaires, moyenne |
| 18 | Lee et al., (2005) (ASS, 14 pays) | Ongo et al., (2022) (ASS, 14 pays) | Contextes spécifiques : conflits, mines, multilinguisme | **36.6** | specifiques, opportunites, multilinguisme, modele, mines, lineaire |
| 19 | Zuze et Reddy (2014) (Afrique du Sud) | Barnett (2013) (Malawi) | Facteurs socio-économiques et inégalités et participation communautaire | **36.6** | communautaire, socio-economiques, participation, lecture, inegalites, facteurs |
| 20 | Kadio (2022) (ASS, 10 pays) | Michelowa (2001) (ASS, 5 pays Burkina Faso, Cameroun, Côte d'Ivoire, Madagascar, Sénégal.) | Contextes spécifiques : conflits, mines, multilinguisme | **36.3** | inegalites, niveaux, determinants, apprentissage, specifiques, scolaires |

> **Comment lire ce tableau ?**
> - **Rang 1** = la paire la plus similaire du corpus entier.
> - **Score** : plus il est élevé, plus les études se ressemblent (sur 100).
> - **Ce qui les rapproche** : les raisons principales de leur proximité.

> **Fichier à consulter :** `result/top_25_similar_pairs.csv` (top 25)
> ou `result/similarity_pairs_detailed.csv` (toutes les paires avec tous les détails).

---

## 6. Analyse dédiée : Résultats et Recommandations

Cette section est **unique** dans l'analyse : elle compare uniquement la dernière colonne
du document source, celle qui contient les résultats et recommandations de chaque étude.

**Pourquoi c'est important ?**
Deux études peuvent traiter du même thème mais arriver à des conclusions opposées,
ou inversement, deux études de thèmes différents peuvent aboutir aux mêmes recommandations.
Cette analyse permet de détecter ces convergences que le score global ne montrerait pas.

**Comment fonctionne le score de convergence ?**
Pour chaque étude, on mesure à quel point ses résultats ressemblent à ceux des autres.
Un score de convergence élevé signifie que plusieurs autres études arrivent aux mêmes conclusions.

> **Étude la plus convergente sur ses résultats :** Ongo et al., (2022)
> avec un score de convergence de **15.2**.
> Ses voisins les plus proches sur les résultats : Nguemkap et Dieng (2022) (29.4%); Mafang et al. (2022) (8.5%); Nguemkap (2023) (7.6%).

### 6a. Paires dont les conclusions se ressemblent le plus

| Rang | Étude 1 | Année | Étude 2 | Année | Même thème ? | Similarité résultats | Mots-clés communs dans les résultats |
|---:|---|---:|---|---:|:---:|---:|---|
| 1 | Nguemkap et Dieng (2022) | 2022 | Ongo et al., (2022) | 2022 | ✓ Oui | **29.4 %** | mathematiques, lecture, scolaires, niveau, famille, specifiques |
| 2 | Armstrong (2015) | 2015 | Kanyongo et Brown (2013) | 2013 | ✓ Oui | **24.2 %** | enseignants, mathematiques, ages, jeunes, formation, ameliorer |
| 3 | Taniguchi (2022) | 2022 | Taniguchi (2024) | 2024 | ✓ Oui | **18.6 %** | enfants, ressources, meilleurs, ceux, ont, petite |
| 4 | Sumida et Kawata (2021) | 2021 | Burger (2011) | 2011 | ✓ Oui | **14.9 %** | zones, rurales, differences, ressources, ecart, urbaines |
| 5 | Kadio et al., (2022) | 2022 | Kadio (2022) | 2022 | ✓ Oui | **13.5 %** | ressources, utilisation, secteur, scolaires, public, negative |
| 6 | Zhang (2006) | 2006 | Sumida et Kawata (2021) | 2021 | ✓ Oui | **13.3 %** | zones, rurales, differences, apprentissage, urbaines, scolaires |
| 7 | Zhang (2006) | 2006 | Burger (2011) | 2011 | ✓ Oui | **12.3 %** | zones, rurales, ressources, differences, urbaines, scolaires |
| 8 | Bennell (2023) | 2023 | Lauchande et al., (2017) | 2017 | ✗ Non | **10.9 %** | cours, socio-economiques, milieux, issus, place, mettre |
| 9 | Yu et Thomas (2008) | 2008 | Kadio (2022) | 2022 | ✓ Oui | **10.4 %** | statut, socio-economique, ressources, parents, differences, ont |
| 10 | Kuecken et al., (2013) | 2013 | Frölich et Michaelowa (2011) | 2011 | ✓ Oui | **10.4 %** | manuels, partage, autres, acces, scolaires, connaissances |
| 11 | Yu et Thomas (2008) | 2008 | Kanyongo, et al., (2006) | 2006 | ✓ Oui | **10.2 %** | soutien, ressources, familial, facteurs, tels, mieux |
| 12 | Dieng et Sy (2020) | 2020 | Figueiredo et Dieng (2016) | 2016 | ✗ Non | **9.9 %** | scolaires, organisations, internationales, gouvernements, explication, encourager |
| 13 | Venkat et Spaull (2015) | 2015 | Kanyongo et Brown (2013) | 2013 | ✓ Oui | **9.7 %** | mathematiques, enseignants, ont, enseignement, connaissances, ayant |
| 14 | Atuhurra (2016) | 2016 | Hungi et Thuku (2009) | 2009 | ✓ Oui | **9.4 %** | prenantes, parties, socio-economique, primaires, politiques, inegalites |
| 15 | Kanyongo, et al., (2006) | 2006 | Kanyongo et Ayieko (2017) | 2017 | ✗ Non | **8.9 %** | ressources, scolaires, predicteur, mieux, facteurs, encourager |

> **Comment lire ce tableau ?**
> - **Similarité résultats** : pourcentage de ressemblance uniquement sur les conclusions.
> - **Même thème ✓** : les deux études sont classées dans le même thème → convergence attendue.
> - **Même thème ✗** : les deux études viennent de thèmes *différents* mais arrivent à des
>   conclusions similaires → convergence surprenante, à investiguer en priorité.

### 6b. Les études dont les conclusions convergent le plus (avec d'autres études)

| Auteur | Année | Score de convergence | Les 3 études aux conclusions les plus proches | Termes dominants dans ses résultats |
|---|---:|---:|---|---|
| Ongo et al., (2022) | 2022 | **15.2** | Nguemkap et Dieng (2022) (29.4%); Mafang et al. (2022) (8.5%); Nguemkap (2023) (7.6%) | lecture, mathematiques, scolaires, famille, caracteristiques |
| Kanyongo et Brown (2013) | 2013 | **13.5** | Armstrong (2015) (24.2%); Venkat et Spaull (2015) (9.7%); Bekkouche et Dupraz (2023) (6.5%) | enseignants, mathematiques, ages, ameliorer, jeunes |
| Nguemkap et Dieng (2022) | 2022 | **13.3** | Ongo et al., (2022) (29.4%); Nguemkap (2023) (5.3%); Kadio (2022) (5.1%) | niveau, variance, totale, lecture, mathematiques |
| Armstrong (2015) | 2015 | **12.5** | Kanyongo et Brown (2013) (24.2%); Lauchande et al., (2017) (7.0%); Wamala et Seruwagi (2012) (6.3%) | enseignants, jeunes, ages, formation, ameliorent |
| Sumida et Kawata (2021) | 2021 | **11.6** | Burger (2011) (14.9%); Zhang (2006) (13.3%); Kadio (2022) (6.7%) | zones, rurales, differences, caracteristiques, apprentissage |
| Burger (2011) | 2011 | **11.0** | Sumida et Kawata (2021) (14.9%); Zhang (2006) (12.3%); Dickerson et al., (2015) (5.9%) | ecart, ressources, differences, zones, rurales |
| Taniguchi (2022) | 2022 | **10.8** | Taniguchi (2024) (18.6%); Bekkouche et Dupraz (2023) (7.4%); Kazima (2014) (6.6%) | enfants, meilleurs, ont, suivi, enseignement |
| Zhang (2006) | 2006 | **10.8** | Sumida et Kawata (2021) (13.3%); Burger (2011) (12.3%); Sanfo (2023) (6.7%) | scolaires, zones, rurales, urbaines, differences |
| Kadio (2022) | 2022 | **10.3** | Kadio et al., (2022) (13.5%); Yu et Thomas (2008) (10.4%); Servaas van der Berg (2008) (6.9%) | parents, statut, socio-economique, differences, sein |
| Taniguchi (2024) | 2024 | **9.6** | Taniguchi (2022) (18.6%); Salah et Saxena (2025) (5.7%); Smith et Barrett (2010) (4.4%) | enfants, ayant, preprimaire, ceux, ressources |
| Yu et Thomas (2008) | 2008 | **9.6** | Kadio (2022) (10.4%); Kanyongo, et al., (2006) (10.1%); Sanfo et al., (2024) (8.1%) | facteurs, montrent, differences, significativement, influencees |
| Kanyongo, et al., (2006) | 2006 | **8.5** | Yu et Thomas (2008) (10.1%); Kanyongo et Ayieko (2017) (8.9%); Zhang (2006) (6.5%) | lecture, ressources, soutien, parental, domicile |
| Lauchande et al., (2017) | 2017 | **8.4** | Bennell (2023) (10.9%); Hanchane et Kadio (2022) (7.4%); Armstrong (2015) (7.0%) | enseignants, socio-economiques, renforcer, issus, milieux |
| Miningou (2022) | 2022 | **8.2** | Hossain et Bertta (2025) (8.5%); Dickerson et al., (2015) (8.4%); Lee et al., (2018) (7.7%) | infrastructures, ecart, mathematiques, filles, montrent |
| Hossain et Bertta (2025) | 2025 | **8.2** | Miningou (2022) (8.5%); Kadio (2025) (8.3%); Kanyongo et Ayieko (2017) (7.8%) | communaute, ressources, scolaires, implication, significativement |

> **Comment lire ce tableau ?**
> - **Score de convergence** : plus il est élevé, plus les conclusions de cette étude
>   sont partagées par d'autres. Une étude très convergente renforce un consensus scientifique.
> - **Les 3 études les plus proches** : les auteurs dont les résultats ressemblent le plus
>   à ceux de cette étude, avec le pourcentage de similarité entre parenthèses.
> - **Termes dominants** : les mots qui reviennent le plus dans les résultats de cette étude.

> **Fichiers à consulter :**
> - `result/results_recommendations_top_pairs.csv` — toutes les paires classées par similarité des résultats
> - `result/results_recommendations_per_study.csv` — profil de convergence de chaque étude

---

## 7. L'étude la plus proche de chaque publication

Pour chaque étude du corpus, l'analyse a identifié l'étude qui lui ressemble le plus.
C'est le **« voisin le plus proche »**.

**Utilité pratique :** si vous lisez une étude et voulez trouver rapidement
la publication la plus similaire à citer ou à comparer, cette table vous donne la réponse directement.

| Étude | Année | Son étude la plus proche | Année | Score /100 | Ce qu'elles ont en commun |
|---|---:|---|---:|---:|---|
| Sanfo (2021) | 2021 | Garrouste (2011) | 2011 | **33.5** | specifiques, multilinguisme, mines, contextes, conflits |
| Garrouste (2011) | 2011 | Sanfo (2021) | 2021 | **33.5** | specifiques, multilinguisme, mines, contextes, conflits |
| Lee et Rudolf (2022) | 2022 | Sanfo et al., (2024) | 2024 | **27.8** | specifiques, contextes, multilinguisme, mines, conflits |
| Salah et Saxena (2025) | 2025 | Sanfo (2021) | 2021 | **30.1** | conflits, specifiques, multilinguisme, mines, lecture |
| Sanfo et al., (2024) | 2024 | Salah et Saxena (2025) | 2025 | **29.7** | conflits, specifiques, contextes, multilinguisme, mines |
| Kuecken et al., (2013) | 2013 | Frölich et Michaelowa (2011) | 2011 | **33.4** | manuels, partage, autres, acces, specifiques |
| Frölich et Michaelowa (2011) | 2011 | Kuecken et al., (2013) | 2013 | **33.4** | manuels, partage, autres, acces, specifiques |
| Zuze et Leibbrandt (2010) | 2010 | Fehrler et al., (2009) | 2009 | **32.4** | ressources, enseignement, enseignants, pedagogiques, specifiques |
| Fehrler et al., (2009) | 2009 | Zuze et Leibbrandt (2010) | 2010 | **32.4** | ressources, enseignement, enseignants, pedagogiques, specifiques |
| Kadio et al., (2022) | 2022 | Kadio (2022) | 2022 | **34.5** | ressources, inegalites, utilisation, specifiques, secteur |
| Kazima et al., (2022) | 2022 | Kazima (2014) | 2014 | **41.5** | mathematiques, enseignement, reformes, enseignants, malawi |
| Hanchane et Kadio (2022) | 2022 | Kadio et al., (2022) | 2022 | **33.8** | apc, ressources, competences, approche, apprentissages |
| Valente (2019) | 2019 | Hanchane et Kadio (2022) | 2022 | **25.6** | specifiques, ressources, politiques, zones, rurales |
| Atuhurra (2016) | 2016 | Kadio et al., (2022) | 2022 | **28.3** | politiques, enseignement, competences, utilisation, specifiques |
| Taylor et Spaull (2015) | 2015 | Crouch et al. (2021) | 2021 | **26.9** | apprentissage, niveaux, statistiques, specifiques, multilinguisme |
| Kazima (2014) | 2014 | Kazima et al., (2022) | 2022 | **41.5** | mathematiques, enseignement, reformes, enseignants, malawi |
| Mioko et Cappelle (2015) | 2015 | Murimba (2005) | 2005 | **39.2** | recherche, politiques, statistique, specifiques, multilinguisme |
| Spaull et Taylor (2015) | 2015 | Mioko et Cappelle (2015) | 2015 | **28.3** | statistique, specifiques, multilinguisme, mines, mesure |
| Murimba (2005) | 2005 | Mioko et Cappelle (2015) | 2015 | **39.2** | recherche, politiques, statistique, specifiques, multilinguisme |
| Dolata (2008) | 2008 | Dieng et Sy (2020) | 2020 | **29.1** | parents, nombre, modele, comparative, specifiques |

> **Fichier à consulter :** `result/nearest_neighbour_per_study.csv` pour toutes les études.

---

## 8. Guide de lecture des graphiques

Trois graphiques ont été générés. Voici comment les lire.

### `temporal_evolution.png` — Évolution dans le temps

Ce fichier contient **deux graphiques** superposés :

**Graphique du haut — Barres empilées :**
- Chaque barre représente une année.
- La hauteur totale = le nombre d'études publiées cette année-là.
- Les couleurs représentent les thèmes : on peut voir quels thèmes dominaient chaque période.
- Le pic est en **2022** avec **13 publications**.

**Graphique du bas — Courbe annuelle :**
- Montre le nombre brut de publications par an (pas le total cumulé).
- Un pic sur la courbe = une année de forte activité de recherche.
- Un creux = peu de publications cette année-là.

### `heatmap_similarity_clusters.png` — Carte thermique de similarité globale

- C'est un tableau de points colorés, où chaque ligne et chaque colonne représente une étude.
- La couleur d'un point indique à quel point les deux études se ressemblent :
  **jaune/clair = très similaires**, **violet/sombre = peu similaires**.
- Les études sont triées par famille : les carrés lumineux sur la diagonale révèlent les clusters.
- Les lignes blanches séparent les différentes familles d'études.

### `heatmap_similarity_results.png` — Carte thermique des résultats uniquement

- Identique à la carte précédente, mais **basée uniquement sur les résultats et recommandations**.
- Si deux études sont claires sur cette carte mais sombres sur l'autre :
  → elles ont des **conclusions similaires bien qu'elles traitent de thèmes différents**.
  C'est le signal le plus intéressant à investiguer.

---

## 9. À quoi sert chaque fichier de données ?

| Fichier | Je l'ouvre quand je veux… |
|---|---|
| `studies_structured.csv` | Voir la liste complète des études avec leur famille (cluster) |
| `top_25_similar_pairs.csv` | Identifier rapidement les 25 paires les plus proches |
| `similarity_pairs_detailed.csv` | Fouiller toutes les comparaisons avec tous les scores détaillés |
| `results_recommendations_top_pairs.csv` | Trouver les études qui arrivent aux mêmes conclusions |
| `results_recommendations_per_study.csv` | Savoir quelles études convergent sur leurs résultats |
| `nearest_neighbour_per_study.csv` | Trouver l'étude la plus proche d'une publication donnée |
| `study_clusters.csv` | Voir le résumé de chaque famille thématique |
| `similarity_matrix_0_100.csv` | Consulter le score entre n'importe quelle paire d'études |

---

## 10. Ce que ces résultats ne disent PAS

Il est important de comprendre les limites de cette analyse pour ne pas sur-interpréter les scores.

**1. Un score élevé ne signifie pas que les études se copient.**
Deux études peuvent aborder le même sujet de manière indépendante et rigoureuse.
Un score élevé indique simplement qu'elles sont proches — pas qu'il y a un problème.

**2. Un score faible ne signifie pas que les études sont sans rapport.**
Si deux études utilisent des vocabulaires très différents pour parler du même phénomène,
l'outil peut sous-estimer leur proximité réelle.

**3. La similarité des résultats ≠ consensus scientifique.**
Deux études peuvent avoir des résultats textuellement proches mais des conclusions
scientifiques opposées (ex. : l'une conclut à un effet positif, l'autre à un effet négatif).
Le score ne lit pas le sens — il compare les mots.

**4. Ces scores sont des outils de tri, pas des verdicts.**
Utilisez-les pour orienter votre lecture et repérer les études à comparer,
mais vérifiez toujours qualitativement les paires identifiées comme très proches.

---

*Rapport généré automatiquement par le pipeline d'analyse de similarité.*
