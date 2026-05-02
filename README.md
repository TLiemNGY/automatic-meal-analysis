# Meal Builder NiceGUI

Application locale en Python pour construire des repas simples en sèche / recomposition musculaire.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Puis ouvrir : http://localhost:8080

## Ce que fait l'app

- Préparer, compléter ou faire le bilan d'une journée.
- Objectifs affichés comme zones utiles plutôt que chiffres rigides.
- Repas maison avec plusieurs ingrédients : protéines, féculents, huile/sauce ou aliment libre.
- Self d'entreprise avec estimations simples et ajout libre.
- Petit-déj, goûter, shaker et cafés au lait.
- Shaker standard : 25 g whey + lait demi-écrémé, 250 ml par défaut.
- Sport en plus : courses prédéfinies, badminton, marche ou dépense personnalisée.
- Barres visuelles vert / jaune / rouge selon la cohérence avec la zone cible.
- Profil affiché dans l’app : homme, 26 ans, 165 cm, 62 kg, objectif sèche/recomposition, métabolisme de base estimé.
- Quantité totale affichée pour les portions : exemple 1,5 × 75 g = environ 112,5 g.
- Export JSON ou CSV dans le dossier `exports/`.

## Tests

```bash
pytest
```
