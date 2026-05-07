# Meal Builder NiceGUI

Application locale en Python pour construire des repas simples en sèche / recomposition musculaire, sans transformer l'alimentation en tableur.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Puis ouvrir : http://localhost:8080

## Profils disponibles

- **Liêm** : homme, 26 ans, 165 cm, 62 kg, objectif summer body / recomposition, marche par défaut 4 km.
- **Mathilde** : femme, 26 ans, 160 cm, 60 kg, objectif perte de gras + tonus bras/abdos/cuisses + fessiers musclés, vélo obligatoire par défaut 1h30, tupperwares maison uniquement.

Le profil se choisit dans **Réglages du jour**. Les aliments, petits-déjeuners, goûters, sports et repères nutritionnels s'adaptent au profil.

## Ce que fait l'app

- Préparer, compléter ou faire le bilan d'une journée.
- Objectifs affichés comme zones utiles plutôt que chiffres rigides.
- Repas maison avec plusieurs ingrédients : protéines, féculents, huile/sauce ou aliment libre.
- Self d'entreprise avec estimations simples et ajout libre pour les profils concernés.
- Petit-déj et plusieurs goûters. Shaker et cafés au lait seulement pour les profils concernés.
- Shaker standard pour Liêm : 25 g whey + lait demi-écrémé, 250 ml par défaut.
- Déplacement par défaut modifiable : marche pour Liêm, vélo pour Mathilde.
- Sports additionnels multiples avec bouton **Ajouter un sport**.
- Barres visuelles vert / jaune / rouge selon la cohérence avec la zone cible.
- Quantité totale affichée pour les portions : exemple 1,5 × 75 g = environ 112,5 g.
- Export JSON ou CSV dans le dossier `exports/`.

## Tests

```bash
pytest
```
