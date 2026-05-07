# Meal Builder NiceGUI

Application Python/NiceGUI pour construire des repas simples en sèche / recomposition musculaire, sans transformer l'alimentation en tableur.

## Installation locale

```bash
pip install -r requirements.txt
```

## Lancement local

```bash
python app.py
```

Puis ouvrir : http://localhost:8080

En local, aucun mot de passe n'est demandé par défaut. Pour tester le mode privé :

```bash
APP_PASSWORD=ton_mot_de_passe python app.py
```

Sous PowerShell :

```powershell
$env:APP_PASSWORD="ton_mot_de_passe"
python app.py
```

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

## Déploiement gratuit sur Render

Le repo contient déjà :

```text
Dockerfile
render.yaml
```

L'app écoute automatiquement le port fourni par Render via la variable `PORT`.

### Étapes

1. Pousse ce repo sur GitHub.
2. Va sur Render et crée un **New Web Service**.
3. Connecte ton repo `automatic-meal-analysis`.
4. Render devrait détecter `render.yaml`.
5. Dans les variables d'environnement, renseigne :

```text
APP_PASSWORD=un_mot_de_passe_long
```

`NICEGUI_STORAGE_SECRET` est généré automatiquement par `render.yaml` si Render l'accepte. Sinon, crée-la manuellement avec une valeur longue et aléatoire.

Exemple :

```text
NICEGUI_STORAGE_SECRET=change-moi-avec-une-longue-chaine-aleatoire
```

6. Déploie.
7. Render donnera une URL publique, accessible depuis téléphone.

### Notes importantes

- Le plan gratuit peut mettre l'app en sommeil après inactivité. Le premier chargement peut donc prendre quelques dizaines de secondes.
- Si `APP_PASSWORD` n'est pas défini, l'app est publique. Pour une URL accessible depuis téléphone, il vaut mieux définir un mot de passe.
- Les exports JSON/CSV sont écrits dans le disque temporaire du serveur. Sur Render gratuit, ne considère pas ces exports comme un stockage durable.

## Tests

```bash
pytest
```
