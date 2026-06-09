from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Macros:
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0
    kcal: float | None = None

    def energy(self) -> float:
        return self.kcal if self.kcal is not None else self.protein * 4 + self.carbs * 4 + self.fat * 9


@dataclass(frozen=True)
class Target:
    protein: float
    carbs: float
    fat: float
    kcal: float

    def ranges(self) -> dict[str, tuple[float, float]]:
        return {
            'protein': (self.protein - 10, self.protein + 10),
            'carbs': (self.carbs - 30, self.carbs + 30),
            'fat': (self.fat - 8, self.fat + 8),
            'kcal': (self.kcal - 120, self.kcal + 120),
        }


TARGETS: Dict[str, Target] = {
    'Repos': Target(130, 200, 55, 1815),
    'Muscu': Target(140, 260, 60, 2140),
    'Badminton 2h': Target(140, 330, 65, 2465),
}

SPORT_EXTRAS: Dict[str, Macros] = {
    'Aucun': Macros(),
    "Course 30 min à 6'/km": Macros(carbs=30, kcal=210),
    "Course 45 min à 6'/km": Macros(carbs=45, kcal=315),
    "Course 30 min à 5'30/km": Macros(carbs=35, kcal=235),
    "Course 45 min à 5'30/km": Macros(carbs=52, kcal=350),
    'Badminton en plus 1h': Macros(carbs=45, kcal=220),
    'Longue marche': Macros(carbs=25, kcal=120),
    'Autre sport': Macros(carbs=0, kcal=0),
}

PROTEINS: Dict[str, Macros] = {
    'Aucune': Macros(),
    'Filet de poulet — 150 g cru': Macros(35, 0, 2, 165),
    'Filet de dinde — 150 g cru': Macros(36, 0, 2, 165),
    'Blanc poulet/dinde vraie viande — 150 g cru': Macros(37, 0, 2.5, 178),
    'Thon au naturel — 120 g égoutté': Macros(29, 0, 1, 125),
    'Steak haché 5 % — 125 g cru': Macros(27, 0, 6, 160),
    'Bavette — 150 g crue': Macros(31, 0, 9, 200),
    'Saumon — 150 g cru': Macros(30, 0, 17, 290),
    'Saumon self — 125 g': Macros(25, 0, 14, 240),
    'Sardines égouttées — 100 g': Macros(25, 0, 11, 205),
    'Œuf — 1 unité': Macros(6.5, 0.5, 5, 72),
    'Steak haché 20 % — 125 g cru': Macros(21, 0, 25, 315),
    'Lardons — 50 g': Macros(8, 0, 11, 130),
}

CARBS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Riz blanc cru — 70 g': Macros(5, 50, 1, 230),
    'Riz complet cru — 70 g': Macros(5, 50, 1.5, 235),
    'Riz rouge cru — 70 g': Macros(5, 50, 1.5, 235),
    'Riz noir cru — 70 g': Macros(5, 50, 1.5, 235),
    'Pâtes normales crues — 75 g': Macros(9, 50, 1.5, 250),
    'Pâtes semi-complètes crues — 75 g': Macros(9, 50, 1.5, 250),
    'Pâtes complètes crues — 75 g': Macros(10, 50, 2, 255),
    'Semoule crue — 70 g': Macros(8, 50, 1, 240),
    'Boulgour cru — 70 g': Macros(8, 50, 1, 240),
    'Sarrasin cru — 75 g': Macros(8, 50, 2, 250),
    'Épeautre cru — 80 g': Macros(10, 50, 2, 260),
    'Lentilles crues — 85 g': Macros(20, 50, 1.5, 295),
    'Lentilles corail crues — 85 g': Macros(21, 50, 1.5, 300),
    'Pomme de terre au four — 300 g crue': Macros(6, 50, 0.5, 230),
    'Nouilles instantanées — 1 paquet 60 g': Macros(7, 52, 14, 360),
}

FATS: Dict[str, Macros] = {
    'Aucune': Macros(),
    'Huile — 1 c. à soupe': Macros(0, 0, 10, 90),
}

BREAKFASTS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Nouilles instantanées — 1 paquet 60 g': Macros(7, 52, 14, 360),
    'Fromage blanc + confiture — 200 g + 20 g': Macros(17, 28, 0, 185),
    'Fromage blanc + flocons d’avoine — 200 g + 50 g': Macros(22, 38, 3.5, 290),
    'Bretzel fromage — 1 portion 100 g': Macros(11.96, 43.04, 10.17, 317.43),
    'Autre petit-déj': Macros(),
}

SNACKS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Banane — 1 unité': Macros(1, 25, 0, 100),
    'Bonbons crocodile — 30 g': Macros(0, 24, 0, 100),
    'Fromage blanc + flocons d’avoine — 200 g + 50 g': Macros(22, 38, 3.5, 290),
    'Fromage blanc normal + flocons — 200 g + 50 g': Macros(21, 38, 9.5, 340),
    'Sushis antigaspi — boîte variée ≈ 15 pièces': Macros(28, 95, 12, 600),
    'Autre goûter': Macros(),
}

MILKS_PER_100ML: Dict[str, Macros] = {
    'Lait demi-écrémé': Macros(3.3, 5, 1.5, 47),
}

SELF_PROTEINS: Dict[str, Macros] = {
    'Poulet — 1 portion self': Macros(35, 0, 3, 180),
    'Saumon — 125 g self': Macros(25, 0, 14, 240),
    'Bavette — 1 portion self': Macros(31, 0, 9, 200),
    'Steak haché 20 % — 1 portion self': Macros(21, 0, 25, 315),
}

SELF_RICE: Dict[str, Macros] = {
    'Portion normale — équiv. 70-80 g riz cru': Macros(5, 50, 1, 230),
    'Grosse portion — équiv. 105-120 g riz cru': Macros(7.5, 75, 1.5, 345),
}

SELF_VEG: Dict[str, Macros] = {
    'Normaux huileux — +5 à 10 g lipides': Macros(2, 8, 7, 105),
    'Très huileux — +10 à 15 g lipides': Macros(2, 8, 13, 160),
}

SELF_SAUCE: Dict[str, Macros] = {
    'Pas de sauce': Macros(),
    'Petite louche — +5 à 10 g lipides': Macros(1, 3, 7, 80),
    'Grosse louche — +10 à 15 g lipides': Macros(2, 6, 12, 140),
}
