from src.data import Macros, TARGETS
from src.nutrition import add_macros, remaining, scale_macros, status_for, target_with_extra_sport


def test_add_macros_uses_declared_kcal():
    total = add_macros([Macros(10, 20, 5, 180), Macros(5, 5, 1, 60)])
    assert total.protein == 15
    assert total.carbs == 25
    assert total.fat == 6
    assert total.kcal == 240


def test_scale_macros():
    assert scale_macros(Macros(10, 20, 5, 200), 1.5) == Macros(15, 30, 7.5, 300)


def test_remaining():
    left = remaining(Macros(100, 200, 40, 1600), TARGETS['Muscu'])
    assert left.protein == 40
    assert left.carbs == 60
    assert left.fat == 20
    assert left.kcal == 540


def test_target_with_extra_sport():
    target = target_with_extra_sport(TARGETS['Repos'], "Course 30 min à 6'/km")
    assert target.carbs == 230
    assert target.kcal == 2025


def test_status_for():
    assert status_for(100, 90, 110) == 'ok'
    assert status_for(85, 90, 110) == 'warn'
    assert status_for(40, 90, 110) == 'bad'
