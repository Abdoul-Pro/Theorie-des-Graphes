# Graphe de connaissances : Modele d'un quartier

Projet de **Theorie des Graphes** — Licence 1 Informatique (L1S2)
Universite Joseph Ki-Zerbo — Annee academique 2025-2026

Sous la supervision de : **Dr Serges SONCFACK**
Groupe 5

---

## Description

Ce projet modelise un quartier (Tampouy) sous forme de **graphe de connaissances oriente**, ou chaque nœud represente une entite (habitant, maison, ecole, commerce, centre de sante, route) et chaque arc represente une relation entre ces entites.

L'objectif est de pouvoir repondre a des questions sur les habitants, leurs lieux de vie, les services qu'ils frequentent et les connexions entre toutes ces entites.

## Structure du projet

```
Code_Python/
├── app.py              ← Application graphique (interface)
├── requirements.txt    ← Dependances Python
├── README.md           ← Ce fichier
└── __pycache__/        ← Cache Python (auto-genere)
```

## Installation

```bash
# Creer un environnement virtuel
python -m venv .venv

# Activer l'environnement
# Windows :
.venv\Scripts\activate
# Linux/Mac :
source .venv/bin/activate

# Installer les dependances
pip install -r requirements.txt
```

## Utilisation

```bash
python app.py
```

L'application graphique (tkinter + matplotlib) propose :
- Un **apercu du graphe** dans la fenetre (redimensionnable)
- Un bouton **Generer et enregistrer l'image** (PNG, choix de l'emplacement via un dialogue)
- Une section **Statistiques** (nombre de noeuds)
- Une section **Noeuds du graphe** (liste coloree par type)
- Interface **dark theme** avec mise en page responsive

## Donnees du graphe

### Noeuds (12)

| Noeud | Type |
|-------|------|
| Quartier Tampouy | Quartier |
| Maison 1, Maison 2 | Maison |
| Fadal, Djemila | Adulte |
| Khalilou | Enfant |
| Idrissa | Adolescent |
| Aboubacar | Personne agee |
| Ecole Primaire | Ecole |
| Boutique Gouemzy | Commerce |
| CSPS Tampouy | Centre de sante |
| Route Principale | Route |

### Relations (13)

| Source | Destination | Relation |
|--------|-------------|----------|
| Maison 1 | Quartier Tampouy | EST_DANS |
| Maison 2 | Quartier Tampouy | EST_DANS |
| Fadal | Maison 1 | HABITE |
| Djemila | Maison 1 | HABITE |
| Khalilou | Maison 1 | HABITE |
| Aboubacar | Maison 2 | HABITE |
| Idrissa | Maison 2 | HABITE |
| Khalilou | Ecole Primaire | FREQUENTE |
| Idrissa | Ecole Primaire | FREQUENTE |
| Fadal | Boutique Gouemzy | TRAVAILLE_DANS |
| Aboubacar | CSPS Tampouy | SE_SOIGNE_A |
| Boutique Gouemzy | Route Principale | EST_SITUE_SUR |
| CSPS Tampouy | Route Principale | EST_SITUE_SUR |

## Proprietes du graphe

| Propriete | Valeur |
|-----------|--------|
| Nombre de noeuds | 12 |
| Nombre d'aretes | 13 |
| Densite | 0.098 |
| Connexe | Oui |
| Diametre | 5 |

### Centralite de degre

| Noeud | Centralite |
|-------|------------|
| Maison 1 | 0.364 |
| Maison 2 | 0.273 |
| Quartier Tampouy | 0.182 |
| Fadal | 0.182 |
| Ecole Primaire | 0.182 |
| Boutique Gouemzy | 0.182 |
| CSPS Tampouy | 0.182 |
| Route Principale | 0.182 |
| Djemila | 0.091 |
| Khalilou | 0.091 |
| Idrissa | 0.091 |
| Aboubacar | 0.091 |

## Questions de competences

Ce projet permet de repondre aux questions suivantes :

1. Quels habitants vivent dans une maison dont au moins un enfant frequente l'ecole primaire ?
2. Quels commerces sont accessibles aux habitants residant sur la meme route qu'un centre de sante ?
3. Quels habitants peuvent etre relies parce qu'ils habitent le meme quartier, frequentent la meme ecole ou utilisent le meme centre de sante ?
4. Quels habitants sont indirectement lies a un commerce par l'intermediaire de la route ?
5. Quels enfants vivent avec un adulte qui travaille dans un commerce du quartier ?
6. Quels habitants partagent les memes infrastructures sans habiter la meme maison ?
7. Quelles maisons sont relyes a un centre de sante par les habitants qui s'y rendent ?
8. Quels habitants sont connectes par une chaine de relations passant par une ecole, un commerce ou un centre de sante ?
9. Quels services sont accessibles a tous les membres d'une meme maison ?
10. Quels sont les chemins reliant un habitant a un commerce ou un centre de sante ?

## Operations sur les graphes

| Operation | Description | Application |
|-----------|-------------|-------------|
| Union | Fusionner deux graphes | Combiner les donnees de deux quartiers |
| Intersection | Garder uniquement les elements communs | Identifier les habitants/infrastructures partages |
| Jointure | Relier deux graphes via une information commune | Lier habitants et ecoles via la frequentation |
| Produit cartesien | Associer chaque element de G1 avec tous ceux de G2 | Etudier toutes les possibilites de relations |
| Produit tensoriel | Combiner deux graphes en nouvelles relations | Analyser qui utilise quoi et comment |

## Domaines d'application

- Urbanisation et planification urbaine
- Gestion municipale et administrative
- Securite et surveillance du quartier
- Gestion des services publics

## Auteurs

Groupe 5 — Licence 1 Informatique — Universite Joseph Ki-Zerbo
