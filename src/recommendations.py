from __future__ import annotations

from src.data import Macros, Target
from src.nutrition import remaining


def warnings(total: Macros, target: Target, self_context: str = '') -> list[str]:
    out: list[str] = []
    ranges = target.ranges()
    if total.protein < ranges['protein'][0]:
        out.append('Protéines un peu basses : ajoute une source simple comme poulet, dinde, thon ou whey.')
    if total.carbs < ranges['carbs'][0]:
        out.append('Glucides bas pour ce type de journée : ajoute plutôt riz, pâtes, pommes de terre ou une banane.')
    if total.fat > ranges['fat'][1]:
        out.append('Lipides hauts aujourd’hui : termine avec poulet/dinde/thon, légumes, et évite huile, œufs, saumon ou sauce.')
    if 'steak' in self_context.lower() or 'sauce' in self_context.lower() or 'huileux' in self_context.lower():
        out.append('Self probablement gras : ce soir, garde un dîner très propre et sans gras ajouté.')
    return out


def dinner_advice(total: Macros, target: Target) -> str:
    left = remaining(total, target)
    if left.fat < 5:
        return 'Dîner conseillé : poulet ou thon + féculent propre + légumes, sans huile ajoutée.'
    if left.carbs > 80:
        return 'Dîner conseillé : 150 g poulet/dinde + 1 à 1,5 portion de riz ou pâtes + légumes.'
    if left.protein > 25:
        return 'Dîner conseillé : une vraie portion de protéine maigre + légumes. Ajoute un peu de féculent si tu as faim.'
    return 'Dîner conseillé : repas simple, plutôt léger, avec légumes et une protéine maigre.'


def daily_comment(total: Macros, target: Target) -> str:
    w = warnings(total, target)
    if not w:
        return 'Bonne journée : cohérente avec une sèche/recomposition, sans rigidité inutile.'
    return 'À corriger : ' + ' '.join(w[:2])


def tomorrow_suggestion(total: Macros, target: Target) -> str:
    ranges = target.ranges()
    if total.fat > ranges['fat'][1]:
        return 'Demain : privilégie viandes maigres, sauce à part, et garde les lipides plus bas.'
    if total.carbs < ranges['carbs'][0]:
        return 'Demain : mets plus de glucides autour du sport pour mieux performer.'
    if total.protein < ranges['protein'][0]:
        return 'Demain : sécurise une portion de protéines à chaque repas.'
    return 'Demain : garde la même structure, elle est simple et efficace.'
