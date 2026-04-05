# Rapport d'interprétation — Analyse avancée de similarité

## Vue d'ensemble
- Nombre total d'études extraites : **82**
- Nombre total de paires comparées : **3321**
- Nombre de clusters détectés : **21**
- Taille moyenne des clusters : **3.9**

## Seuils d'interprétation du score global (/100)
| Seuil | Signification |
|---|---|
| ≥ 50 | Similarité forte dans ce corpus |
| 40 – 49 | Similarité assez forte |
| 30 – 39 | Similarité modérée |
| < 30 | Similarité faible à modérée |

## Nouvelles dimensions d'analyse
- **`sim_results`** : similarité dédiée à la colonne *Résultats & Recommandations* (TF-IDF indépendant)
- **`evolution_temporelle.png`** : barres empilées par thème + courbe cumulative
- **`top_similarite_resultats_recommandations.csv`** : top-50 paires les plus proches sur les conclusions

## Top 20 des paires les plus similaires
| Rang | Étude 1 | Étude 2 | Thème | Score /100 | %ile | Mots-clés communs |
|---|---|---|---|---:|---:|---|
| 1 | Nguemkap et Dieng (2022) (Cameroun) | Ongo et al., (2022) (ASS, 14 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 51.71 | 100.00 | mathematiques, lecture, scolaires, specifiques, niveau, famille |
| 2 | Sumida et Kawata (2021) (ASS, 15 pays) | Burger (2011) (Zambie) | Facteurs socio-économiques et inégalités et participation communautaire | 46.88 | 99.97 | zones, rurales, differences, ressources, ecart, socio-economiques |
| 3 | Taniguchi (2022) (ASS, 15 pays) | Taniguchi (2024) (ASS, 15 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 44.04 | 99.94 | enfants, ressources, meilleurs, defavorises, ceux, apprentissage |
| 4 | Miningou (2022) (ASS 10 pays) | Sumida et Kawata (2021) (ASS, 15 pays) | Facteurs socio-économiques et inégalités et participation communautaire | 42.99 | 99.91 | ecart, apprentissage, socio-economiques, participation, inegalites, facteurs |
| 5 | Kazima et al., (2022) (Malawi) | Kazima (2014) (Botswana, Malawi et Zambie) | Contextes spécifiques : conflits, mines, multilinguisme | 41.54 | 99.88 | mathematiques, enseignement, reformes, enseignants, malawi, ameliorer |
| 6 | Miningou (2022) (ASS 10 pays) | Burger (2011) (Zambie) | Facteurs socio-économiques et inégalités et participation communautaire | 39.98 | 99.85 | ecart, ressources, socio-economiques, participation, inegalites, facteurs |
| 7 | Ongo et al., (2022) (ASS, 14 pays) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 39.61 | 99.82 | scolaires, inegalites, specifiques, sein, differences, determinants |
| 8 | Smith et Barrett (2010) (ASS, 6 pays) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 39.44 | 99.79 | apprentissage, ressources, inegalites, specifiques, politiques, determinants |
| 9 | Mioko et Cappelle (2015) (ASS, 11 pays) | Murimba (2005) (ASS, 15 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 39.22 | 99.76 | recherche, politiques, statistique, specifiques, multilinguisme, mines |
| 10 | Armstrong (2015) (ASS, 15 pays) | Kanyongo et Brown (2013) (Namibie) | Principaux résultats et recommandations de politique éducative | 38.74 | 99.73 | enseignants, mathematiques, principaux, politique, educative, ages |
| 11 | Zhang (2006) (ASS, 14 pays) | Sumida et Kawata (2021) (ASS, 15 pays) | Facteurs socio-économiques et inégalités et participation communautaire | 38.11 | 99.70 | rurales, zones, apprentissage, facteurs, differences, urbaines |
| 12 | Smith et Barrett (2010) (ASS, 6 pays) | Ongo et al., (2022) (ASS, 14 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 37.97 | 99.67 | lecture, apprentissage, scolaires, specifiques, opportunites, niveaux |
| 13 | Nguemkap et Dieng (2022) (Cameroun) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 37.75 | 99.64 | niveau, inegalites, determinants, specifiques, socio-economique, sein |
| 14 | Hungi et Thuku (2009) (Kenya) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 37.53 | 99.61 | inegalites, socio-economique, determinants, apprentissage, specifiques, sociale |
| 15 | Sanfo (2020) (Burkina Faso) | Foueka et Elomo (2022) (ASS, 10 pays) | Principaux résultats et recommandations de politique éducative | 37.43 | 99.58 | formation, principaux, politique, educative, niveaux, modele |
| 16 | Lee et al., (2005) (ASS, 14 pays) | Kadio (2022) (ASS, 10 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 37.04 | 99.55 | inegalites, ressources, determinants, apprentissage, specifiques, opportunites |
| 17 | Miningou et al., (2019) (ASS 10 pays) | Avom et al., (2021) (ASS, 10 pays) | Efficience et efficacité des systèmes éducatifs | 36.70 | 99.52 | efficience, efficacite, ressources, politiques, primaires, moyenne |
| 18 | Lee et al., (2005) (ASS, 14 pays) | Ongo et al., (2022) (ASS, 14 pays) | Contextes spécifiques : conflits, mines, multilinguisme | 36.65 | 99.49 | specifiques, opportunites, multilinguisme, modele, mines, lineaire |
| 19 | Zuze et Reddy (2014) (Afrique du Sud) | Barnett (2013) (Malawi) | Facteurs socio-économiques et inégalités et participation communautaire | 36.59 | 99.46 | communautaire, socio-economiques, participation, lecture, inegalites, facteurs |
| 20 | Kadio (2022) (ASS, 10 pays) | Michelowa (2001) (ASS, 5 pays Burkina Faso, Cameroun, Côte d'Ivoire, Madagascar, Sénégal.) | Contextes spécifiques : conflits, mines, multilinguisme | 36.26 | 99.43 | inegalites, niveaux, determinants, apprentissage, specifiques, scolaires |

## Principaux clusters détectés
| Cluster | Taille | Thème dominant | Sous-thème dominant | Mots-clés | Exemples d'auteurs |
|---:|---:|---|---|---|---|
| 1 | 19 | Contextes spécifiques : conflits, mines, multilinguisme | Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage | apprentissage, inegalites, determinants, lecture, specifiques, facteurs | Spaul (2011); Yu et Thomas (2008); Hungi et Thuku (2009); Taniguchi (2022); Smith et Barrett (2010) |
| 3 | 13 | Facteurs socio-économiques et inégalités et participation communautaire | Facteurs socio-économiques et inégalités et participation communautaire | facteurs, socio-economiques, participation, communautaire, inegalites, scolaires | Dickerson et al., (2015); Kyei (2021); Miningou (2022); Zuze et Reddy (2014); Barnett (2013) |
| 2 | 11 | Principaux résultats et recommandations de politique éducative | Principaux résultats et recommandations de politique éducative | enseignants, principaux, politique, educative, formation, ameliorer | Wamala et Seruwagi (2012); Lee et al., (2018); Armstrong (2015); Conto et al., (2023); Sanfo (2020) |
| 0 | 6 | Contextes spécifiques : conflits, mines, multilinguisme | Mesure de la qualité de l’éducation et analyse comparative | comparative, contextes, specifiques, conflits, mines, multilinguisme | Mioko et Cappelle (2015); Spaull et Taylor (2015); Murimba (2005); Dolata (2008); Sandefur (2017) |
| 4 | 4 | Efficience et efficacité des systèmes éducatifs | Efficience et efficacité des systèmes éducatifs | efficience, efficacite, ressources, apprentissage, politiques, etablissements | Miningou et al., (2019); Avom et al., (2021); Figueiredo et Dieng (2016); Kouamo (2024) |
| 7 | 4 | Contextes spécifiques : conflits, mines, multilinguisme | Ressources pédagogiques et infrastructures | ressources, manuels, acces, contextes, specifiques, pedagogiques | Kuecken et al., (2013); Frölich et Michaelowa (2011); Zuze et Leibbrandt (2010); Fehrler et al., (2009) |
| 6 | 3 | Contextes spécifiques : conflits, mines, multilinguisme | Politiques éducatives et réformes | apc, competences, politiques, ressources, contextes, specifiques | Kadio et al., (2022); Hanchane et Kadio (2022); Atuhurra (2016) |
| 8 | 3 | Contextes spécifiques : conflits, mines, multilinguisme | Contextes spécifiques : conflits, mines, multilinguisme | conflits, contextes, specifiques, mines, multilinguisme, mathematiques | Sanfo (2021); Garrouste (2011); Salah et Saxena (2025) |
| 9 | 3 | Contextes spécifiques : conflits, mines, multilinguisme | Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage | cours, apprentissage, supplementaires, inegalites, particuliers, incidence | Bennell (2023); Paviot et al., (2008); Crouch et al. (2021) |
| 14 | 3 | Contextes spécifiques : conflits, mines, multilinguisme | Déterminants de la qualité de l’éducation et inégalités d’opportunités d’apprentissage | mathematiques, francophones, determinants, inegalites, apprentissage, cameroun | Armand et al., (2024); Medu et Rowlands (2022); Bekkouche et Dupraz (2023) |

## Voisin le plus proche (extrait — 15 premières études)
| ID | Auteur | Année | Voisin le plus proche | Année voisin | Score /100 | Mots-clés |
|---:|---|---:|---|---:|---:|---|
| 1 | Sanfo (2021) | 2021 | Garrouste (2011) | 2011 | 33.47 | specifiques, multilinguisme, mines, contextes, conflits |
| 2 | Garrouste (2011) | 2011 | Sanfo (2021) | 2021 | 33.47 | specifiques, multilinguisme, mines, contextes, conflits |
| 3 | Lee et Rudolf (2022) | 2022 | Sanfo et al., (2024) | 2024 | 27.81 | specifiques, contextes, multilinguisme, mines, conflits |
| 4 | Salah et Saxena (2025) | 2025 | Sanfo (2021) | 2021 | 30.05 | conflits, specifiques, multilinguisme, mines, lecture |
| 5 | Sanfo et al., (2024) | 2024 | Salah et Saxena (2025) | 2025 | 29.72 | conflits, specifiques, contextes, multilinguisme, mines |
| 6 | Kuecken et al., (2013) | 2013 | Frölich et Michaelowa (2011) | 2011 | 33.44 | manuels, partage, autres, acces, specifiques |
| 7 | Frölich et Michaelowa (2011) | 2011 | Kuecken et al., (2013) | 2013 | 33.44 | manuels, partage, autres, acces, specifiques |
| 8 | Zuze et Leibbrandt (2010) | 2010 | Fehrler et al., (2009) | 2009 | 32.38 | ressources, enseignement, enseignants, pedagogiques, specifiques |
| 9 | Fehrler et al., (2009) | 2009 | Zuze et Leibbrandt (2010) | 2010 | 32.38 | ressources, enseignement, enseignants, pedagogiques, specifiques |
| 10 | Kadio et al., (2022) | 2022 | Kadio (2022) | 2022 | 34.46 | ressources, inegalites, utilisation, specifiques, secteur |
| 11 | Kazima et al., (2022) | 2022 | Kazima (2014) | 2014 | 41.54 | mathematiques, enseignement, reformes, enseignants, malawi |
| 12 | Hanchane et Kadio (2022) | 2022 | Kadio et al., (2022) | 2022 | 33.84 | apc, ressources, competences, approche, apprentissages |
| 13 | Valente (2019) | 2019 | Hanchane et Kadio (2022) | 2022 | 25.63 | specifiques, ressources, politiques, zones, rurales |
| 14 | Atuhurra (2016) | 2016 | Kadio et al., (2022) | 2022 | 28.26 | politiques, enseignement, competences, utilisation, specifiques |
| 15 | Taylor et Spaull (2015) | 2015 | Crouch et al. (2021) | 2021 | 26.92 | apprentissage, niveaux, statistiques, specifiques, multilinguisme |

## Limites
- Le score mesure une proximité textuelle et structurelle, pas une équivalence scientifique.
- Deux études peuvent être très proches sur la méthode mais diverger sur les conclusions.
- `sim_results` évalue spécifiquement les résultats ; une valeur élevée sans score global élevé indique des conclusions similaires dans des contextes différents.
- Les scores sont des **outils de tri et de lecture**, à vérifier qualitativement.
