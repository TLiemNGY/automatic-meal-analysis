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
    'Pois chiches cuits — 250 g': Macros(18, 50, 7, 330),
    'Haricots rouges cuits — 250 g': Macros(20, 50, 2, 295),
    'Nouilles instantanées — 1 paquet 60 g': Macros(7, 52, 14, 360),
}

FATS: Dict[str, Macros] = {
    'Aucune': Macros(),
    'Huile — 1 c. à soupe': Macros(0, 0, 10, 90),
}

BREAKFASTS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Nouilles instantanées — 1 paquet 60 g': Macros(7, 52, 14, 360),
    'Fromage blanc + confiture — 150 g + 20 g': Macros(13, 26, 0, 160),
    'Fromage blanc + flocons d’avoine — 150 g + 50 g': Macros(18, 36, 3.5, 265),
    'Bretzel fromage — 1 portion 100 g': Macros(11.96, 43.04, 10.17, 317.43),
    'Autre petit-déj': Macros(),
}

SNACKS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Banane — 1 unité': Macros(1, 25, 0, 100),
    'Bonbons crocodile — 30 g': Macros(0, 24, 0, 100),
    'Fromage blanc + flocons d’avoine — 150 g + 50 g': Macros(18, 36, 3.5, 265),
    'Fromage blanc normal + flocons — 150 g + 50 g': Macros(17, 36, 8, 303),
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

# ---------------------------------------------------------------------------
# Profils utilisateur
# ---------------------------------------------------------------------------
# Les profils gardent l'app simple : mêmes écrans, mais repères, aliments et
# déplacements par défaut adaptés à la personne sélectionnée.

LIEM_PROFILE = {
    'display_name': 'Liêm',
    'sex': 'Homme',
    'age': 26,
    'height_cm': 165,
    'weight_kg': 62,
    'goal': 'summer body / recomposition : abdos visibles + densité musculaire',
    'bmr_kcal': round(10 * 62 + 6.25 * 165 - 5 * 26 + 5),
    'targets': TARGETS,
    'proteins': PROTEINS,
    'carbs': CARBS,
    'fats': FATS,
    'breakfasts': BREAKFASTS,
    'snacks': SNACKS,
    'sports': SPORT_EXTRAS,
    'default_day': 'Muscu',
    'uses_self': True,
    'uses_shaker': True,
    'uses_coffee': True,
    'default_movement': {
        'label': 'Marche',
        'unit': 'km',
        'default': 4.0,
        'kcal_per_unit': 45.0,
        'description': 'Les repères de Liêm supposent environ 4 km de marche dans la journée.',
    },
}

MATHILDE_TARGETS: Dict[str, Target] = {
    # Repères de départ volontairement pratiques : assez de protéines, déficit
    # modéré, glucides modulés selon l'activité. À affiner avec l'évolution du
    # poids, des mensurations, de la faim et des performances.
    'Repos': Target(120, 190, 50, 1690),
    'Renfo musculaire 1h': Target(120, 220, 55, 1855),
    'Badminton 2h': Target(120, 280, 55, 2095),
    'Piscine 45 min': Target(120, 230, 55, 1915),
    'Course 45 min': Target(120, 250, 55, 2015),
}

MATHILDE_PROTEINS: Dict[str, Macros] = {
    'Aucune': Macros(),
    'Filet de poulet — 150 g cru': Macros(35, 0, 2, 165),
    'Filet de dinde — 150 g cru': Macros(36, 0, 2, 165),
    'Tofu ferme — 150 g': Macros(18, 3, 12, 190),
    'Tofu soyeux — 150 g': Macros(7.5, 3, 4.5, 85),
    'Œuf — 1 unité': Macros(6.5, 0.5, 5, 72),
    'Sardines égouttées — 100 g': Macros(25, 0, 11, 205),
    'Thon au naturel — 120 g égoutté': Macros(29, 0, 1, 125),
    'Saumon — 150 g cru': Macros(30, 0, 17, 290),
    'Poisson blanc — 150 g cru': Macros(30, 0, 2, 145),
    'Lardons — 50 g': Macros(8, 0, 11, 130),
}

MATHILDE_CARBS: Dict[str, Macros] = CARBS

MATHILDE_BREAKFASTS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Fromage blanc 100 g + 1 banane': Macros(9, 29, 0, 150),
    'Pain Poilâne 1 tranche + Kiri + fruit': Macros(8, 42, 7, 260),
    'Pain Poilâne 1 tranche + œuf + fruit': Macros(12, 40, 7, 270),
    'Pain Poilâne 1 tranche + œuf + fruit + Kiri': Macros(15, 41, 12, 330),
    'Autre petit-déj': Macros(),
}

MATHILDE_SNACKS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Fromage blanc 100 g + 1 banane': Macros(9, 29, 0, 150),
    'Pain Poilâne 1 tranche + Kiri + fruit': Macros(8, 42, 7, 260),
    'Pain Poilâne 1 tranche + œuf + fruit': Macros(12, 40, 7, 270),
    'Pain Poilâne 1 tranche + œuf + fruit + Kiri': Macros(15, 41, 12, 330),
    'Mini-viennoiserie — 1 pièce': Macros(2, 16, 6, 125),
    'Pomme — 1 unité': Macros(0, 20, 0, 80),
    'Autre goûter': Macros(),
}

MATHILDE_SPORTS: Dict[str, Macros] = {
    'Aucun': Macros(),
    'Badminton 2h': Macros(carbs=60, kcal=420),
    'Renfo musculaire 1h': Macros(carbs=30, kcal=220),
    'Piscine 45 min': Macros(carbs=35, kcal=260),
    'Course à pied 45 min': Macros(carbs=50, kcal=360),
    'Autre sport': Macros(carbs=0, kcal=0),
}

MATHILDE_PROFILE = {
    'display_name': 'Mathilde',
    'sex': 'Femme',
    'age': 26,
    'height_cm': 160,
    'weight_kg': 60,
    'goal': 'perdre du gras, affiner les cuisses, bras/abdos/cuisses plus toniques, fessiers plus musclés',
    'bmr_kcal': round(10 * 60 + 6.25 * 160 - 5 * 26 - 161),
    'targets': MATHILDE_TARGETS,
    'proteins': MATHILDE_PROTEINS,
    'carbs': MATHILDE_CARBS,
    'fats': FATS,
    'breakfasts': MATHILDE_BREAKFASTS,
    'snacks': MATHILDE_SNACKS,
    'sports': MATHILDE_SPORTS,
    'default_day': 'Renfo musculaire 1h',
    'uses_self': False,
    'uses_shaker': False,
    'uses_coffee': False,
    'default_movement': {
        'label': 'Vélo obligatoire',
        'unit': 'h',
        'default': 1.5,
        'kcal_per_unit': 180.0,
        'description': 'Les repères de Mathilde supposent environ 1h30 de vélo dans la journée.',
    },
}

PROFILES = {
    'Liêm': LIEM_PROFILE,
    'Mathilde': MATHILDE_PROFILE,
}
