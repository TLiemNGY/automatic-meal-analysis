from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from src.data import Macros, Target, SPORT_EXTRAS


def add_macros(items: Iterable[Macros]) -> Macros:
    p = c = f = k = 0.0
    for item in items:
        p += item.protein
        c += item.carbs
        f += item.fat
        k += item.energy()
    return Macros(round(p, 1), round(c, 1), round(f, 1), round(k, 0))


def scale_macros(item: Macros, factor: float) -> Macros:
    return Macros(
        protein=round(item.protein * factor, 1),
        carbs=round(item.carbs * factor, 1),
        fat=round(item.fat * factor, 1),
        kcal=round(item.energy() * factor, 0),
    )


def target_with_extra_sport(target: Target, sport_name: str) -> Target:
    extra = SPORT_EXTRAS.get(sport_name, Macros())
    return Target(
        protein=target.protein,
        carbs=target.carbs + extra.carbs,
        fat=target.fat,
        kcal=target.kcal + extra.energy(),
    )


def remaining(total: Macros, target: Target) -> Macros:
    return Macros(
        protein=round(target.protein - total.protein, 1),
        carbs=round(target.carbs - total.carbs, 1),
        fat=round(target.fat - total.fat, 1),
        kcal=round(target.kcal - total.energy(), 0),
    )


def status_for(value: float, low: float, high: float) -> str:
    if low <= value <= high:
        return 'ok'
    margin = high - low
    if low - margin * 0.5 <= value <= high + margin * 0.5:
        return 'warn'
    return 'bad'


def export_dict(total: Macros, target: Target) -> dict:
    return {
        'total': asdict(total),
        'target_reference': asdict(target),
        'target_ranges': target.ranges(),
        'remaining_vs_reference': asdict(remaining(total, target)),
    }
