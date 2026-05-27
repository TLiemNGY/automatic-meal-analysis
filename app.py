from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from nicegui import app, ui

from src.data import (
    BREAKFASTS, CARBS, FATS, MILKS_PER_100ML, PROTEINS, SELF_PROTEINS, SELF_RICE,
    SELF_SAUCE, SELF_VEG, SNACKS, SPORT_EXTRAS, TARGETS, Macros, Target,
)
from src.nutrition import add_macros, export_dict, scale_macros, status_for
from src.recommendations import daily_comment, dinner_advice, tomorrow_suggestion, warnings

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / 'exports'
EXPORT_DIR.mkdir(exist_ok=True)
app.add_static_files('/exports', str(EXPORT_DIR))

ui.add_head_html('''
<style>
:root{--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--soft:#f8fafc;--blue:#2563eb;--green:#16a34a;--amber:#f59e0b;--red:#dc2626;--good:#dcfce7;--warn:#fef3c7;--bad:#fee2e2;}
body{background:#f5f7fb;color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.nicegui-content{padding:0!important}.app-shell{min-height:100vh;display:grid;grid-template-columns:280px 1fr}.sidebar{background:linear-gradient(180deg,#08111f,#172033);color:white;padding:28px 20px}.brand{font-size:24px;font-weight:900;letter-spacing:-.04em}.brand-sub{color:#b8c2d6;font-size:13px;line-height:1.45;margin:8px 0 28px}.nav-link{width:100%;padding:13px 14px;border-radius:14px;color:#dbe5f7;text-decoration:none;display:block;margin-bottom:8px;font-weight:750}.nav-link:hover{background:rgba(255,255,255,.10)}.nav-active{background:white;color:#111827;box-shadow:0 12px 30px rgba(0,0,0,.18)}.main{padding:36px 48px 70px;max-width:1280px;width:100%}.hero{margin-bottom:24px}.h1{font-size:40px;font-weight:900;letter-spacing:-.05em;line-height:1.05;margin:0}.subtitle{font-size:15px;color:var(--muted);margin-top:10px;max-width:740px;line-height:1.55}.card{background:white;border:1px solid var(--line);border-radius:24px;padding:22px;box-shadow:0 16px 40px rgba(15,23,42,.055);margin-bottom:18px}.section-title{font-size:21px;font-weight:850;letter-spacing:-.03em;margin:0 0 14px}.small{color:var(--muted);font-size:13px;line-height:1.45}.metric-grid{display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));gap:16px}.metric{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px}.metric-label{color:var(--muted);font-size:13px;font-weight:750}.metric-value{font-size:34px;font-weight:900;letter-spacing:-.05em;margin-top:4px}.range-wrap{margin:18px 0 24px}.range-head{display:flex;justify-content:space-between;gap:12px;align-items:baseline;margin-bottom:8px}.range-title{font-weight:850}.range-note{color:var(--muted);font-size:13px}.range-track{height:18px;background:#edf2f7;border-radius:999px;position:relative;overflow:hidden}.range-zone{height:18px;position:absolute;top:0;border-radius:999px}.range-fill{height:18px;position:absolute;left:0;top:0;border-radius:999px}.range-mid{width:3px;height:22px;background:#0f172a;position:absolute;top:-2px;border-radius:2px;opacity:.7}.range-labels{display:flex;justify-content:space-between;color:var(--muted);font-size:12px;margin-top:6px}.status-ok .range-zone{background:#bbf7d0}.status-ok .range-fill{background:#16a34a}.status-warn .range-zone{background:#fde68a}.status-warn .range-fill{background:#f59e0b}.status-bad .range-zone{background:#fecaca}.status-bad .range-fill{background:#dc2626}.pill{display:inline-flex;align-items:center;border-radius:999px;padding:4px 9px;font-size:12px;font-weight:800}.pill-ok{background:var(--good);color:#166534}.pill-warn{background:var(--warn);color:#92400e}.pill-bad{background:var(--bad);color:#991b1b}.box{padding:14px 16px;border-radius:16px;margin:8px 0;border:1px solid}.box-ok{background:#f0fdf4;border-color:#bbf7d0;color:#166534}.box-warn{background:#fffbeb;border-color:#fde68a;color:#92400e}.box-bad{background:#fef2f2;border-color:#fecaca;color:#991b1b}.box-info{background:#eff6ff;border-color:#bfdbfe;color:#1e3a8a}.q-field--outlined .q-field__control{border-radius:14px!important;background:#f8fafc}@media(max-width:900px){.app-shell{grid-template-columns:1fr}.main{padding:26px 18px}.metric-grid{grid-template-columns:1fr 1fr}.h1{font-size:34px}}
</style>
''', shared=True)

PROFILE = {
    'sex': 'Homme',
    'age': 26,
    'height_cm': 165,
    'weight_kg': 62,
    'goal': 'sèche / recomposition musculaire : abdos visibles + densité musculaire',
}
BMR_KCAL = round(10 * PROFILE['weight_kg'] + 6.25 * PROFILE['height_cm'] - 5 * PROFILE['age'] + 5)


def custom_state():
    return {'name': '', 'protein': 0.0, 'carbs': 0.0, 'fat': 0.0, 'kcal': 0.0}

state = {
    'day': 'Muscu',
    'walk_enabled': True, 'walk_km': 4.0,
    'sports': [],
    'self': False, 'self_protein': list(SELF_PROTEINS)[0], 'self_rice': list(SELF_RICE)[0], 'self_veg': list(SELF_VEG)[0], 'self_sauce': list(SELF_SAUCE)[0], 'self_custom': custom_state(),
    'breakfast': 'Aucun', 'breakfast_custom': custom_state(),
    'coffee_count': 0, 'coffee_milk_ml': 60,
    'snacks': [],
    'shaker': False, 'shaker_ml': 250, 'shaker_custom': custom_state(),
    'meals': {'Déjeuner': [], 'Dîner': []},
    'custom': custom_state(),
}


def refresh(): ui.navigate.reload()
def setv(key, value): state[key] = value; refresh()

def custom_macros(d: dict) -> Macros:
    kcal = d.get('kcal') or None
    return Macros(float(d.get('protein') or 0), float(d.get('carbs') or 0), float(d.get('fat') or 0), kcal)

def macro_from_select(source: dict[str, Macros], name: str, portions: float = 1.0) -> Macros:
    return scale_macros(source.get(name, Macros()), portions)

def coffee_macros() -> Macros:
    return scale_macros(MILKS_PER_100ML['Lait demi-écrémé'], state['coffee_count'] * state['coffee_milk_ml'] / 100)

def shaker_macros() -> Macros:
    if not state['shaker']: return custom_macros(state['shaker_custom'])
    whey = Macros(20, 2, 1.5, 100)
    milk = scale_macros(MILKS_PER_100ML['Lait demi-écrémé'], state['shaker_ml'] / 100)
    return add_macros([whey, milk, custom_macros(state['shaker_custom'])])

def self_macros() -> Macros:
    if not state['self']: return custom_macros(state['self_custom'])
    return add_macros([SELF_PROTEINS[state['self_protein']], SELF_RICE[state['self_rice']], SELF_VEG[state['self_veg']], SELF_SAUCE[state['self_sauce']], custom_macros(state['self_custom'])])

def breakfast_macros() -> Macros:
    return add_macros([BREAKFASTS[state['breakfast']], custom_macros(state['breakfast_custom'])])

def snack_macros() -> Macros:
    items: list[Macros] = []
    for row in state['snacks']:
        if row.get('name') == 'Autre goûter':
            items.append(custom_macros(row['custom']))
        else:
            items.append(macro_from_select(SNACKS, row.get('name', 'Aucun'), row.get('qty', 1.0)))
    return add_macros(items)


def add_snack():
    default = 'Bonbons crocodile — 30 g' if 'Bonbons crocodile — 30 g' in SNACKS else [x for x in SNACKS if x != 'Aucun'][0]
    state['snacks'].append({'id': str(uuid4()), 'name': default, 'qty': 1.0, 'custom': custom_state()})
    refresh()


def remove_snack(item_id: str):
    state['snacks'] = [x for x in state['snacks'] if x['id'] != item_id]
    refresh()

def ingredient_options(kind: str):
    return {'Protéine': list(PROTEINS), 'Féculent': list(CARBS), 'Huile / sauce': list(FATS)}[kind]

def meal_macros(title: str) -> Macros:
    items: list[Macros] = []
    for row in state['meals'][title]:
        if row['kind'] == 'Protéine': items.append(macro_from_select(PROTEINS, row['name'], row['qty']))
        elif row['kind'] == 'Féculent': items.append(macro_from_select(CARBS, row['name'], row['qty']))
        elif row['kind'] == 'Huile / sauce': items.append(macro_from_select(FATS, row['name'], row['qty']))
        elif row['kind'] == 'Autre': items.append(custom_macros(row['custom']))
    return add_macros(items)

def total_macros(include_custom: bool = False) -> Macros:
    items = [breakfast_macros(), coffee_macros(), self_macros(), meal_macros('Déjeuner') if not state['self'] else Macros(), meal_macros('Dîner'), snack_macros(), shaker_macros()]
    if include_custom: items.append(custom_macros(state['custom']))
    return add_macros(items)

def sport_row_extra(row: dict) -> Macros:
    name = row.get('name', 'Aucun')
    if name == 'Autre sport':
        kcal = float(row.get('kcal') or 0)
        return Macros(carbs=round(kcal / 7.0, 0), kcal=kcal)  # compensation simple, surtout en glucides
    return SPORT_EXTRAS.get(name, Macros())


WALK_BASELINE_KM = 4.0
WALK_KCAL_PER_KM = 40.0


def walking_adjustment() -> Macros:
    # Les objectifs de base supposent déjà environ 4 km de marche dans une journée normale.
    # On ajuste donc seulement l'écart par rapport à ce repère.
    km = float(state['walk_km'] or 0) if state.get('walk_enabled', True) else 0.0
    delta_km = km - WALK_BASELINE_KM
    kcal = delta_km * WALK_KCAL_PER_KM
    carbs = round(kcal / 7.0, 0)
    return Macros(carbs=carbs, kcal=kcal)


def sports_extra() -> Macros:
    return add_macros([sport_row_extra(row) for row in state['sports']])


def current_target() -> Target:
    base = TARGETS[state['day']]
    extra = add_macros([sports_extra(), walking_adjustment()])
    return Target(base.protein, max(0, base.carbs + extra.carbs), base.fat, max(0, base.kcal + extra.energy()))


def page_shell(active: str, render):
    with ui.element('div').classes('app-shell'):
        with ui.element('aside').classes('sidebar'):
            ui.html('<div class="brand">Meal Builder</div><div class="brand-sub">Sèche / recomposition, simple et propre.</div>')
            for label, url in [('Préparer','/'),('Compléter','/completer'),('Bilan','/bilan')]:
                ui.link(label, url).classes('nav-link nav-active' if label == active else 'nav-link')
            ui.separator().classes('my-5 opacity-30')
            ui.label('Repères rapides').classes('text-sm text-blue-100 font-bold')
            ui.label('1 portion protéine ≈ 30-35 g').classes('text-xs text-blue-200 mt-2')
            ui.label('1 portion féculent ≈ 50 g glucides').classes('text-xs text-blue-200 mt-1')
        with ui.element('main').classes('main'):
            render()



def profile_card():
    with ui.card().classes('card w-full'):
        ui.label('Profil utilisé par l’app').classes('section-title')
        ui.html(f"""
        <div style="display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:14px">
          <div class="metric" style="padding:14px 16px">
            <div class="metric-label">Profil</div>
            <div style="font-size:16px;font-weight:500;color:#334155;margin-top:4px">{PROFILE['sex']}, {PROFILE['age']} ans</div>
          </div>
          <div class="metric" style="padding:14px 16px">
            <div class="metric-label">Taille / poids</div>
            <div style="font-size:16px;font-weight:500;color:#334155;margin-top:4px">{PROFILE['height_cm']} cm · {PROFILE['weight_kg']} kg</div>
          </div>
          <div class="metric" style="padding:14px 16px">
            <div class="metric-label">Objectif</div>
            <div style="font-size:16px;font-weight:500;color:#334155;margin-top:4px;line-height:1.25">Summer body · recomposition</div>
          </div>
          <div class="metric" style="padding:14px 16px">
            <div class="metric-label">Métabolisme de base estimé</div>
            <div style="font-size:16px;font-weight:500;color:#334155;margin-top:4px">≈ {BMR_KCAL} kcal/j</div>
          </div>
        </div>
        <div class="small mt-3">Calcul du métabolisme de base : formule Mifflin-St Jeor. Ces infos servent juste de contexte ; les repères de repas restent la partie importante.</div>
        """)


def serving_hint(name: str, qty: float) -> str:
    import re
    if name in {'Aucune', 'Aucun'}:
        return ''
    tail = name.split('—', 1)[1].strip() if '—' in name else name
    grams = re.findall(r'(\d+(?:[,.]\d+)?)\s*g\b', tail, re.IGNORECASE)
    if grams:
        amount = float(grams[-1].replace(',', '.')) * qty
        unit = 'g'
    else:
        m = re.search(r'(\d+(?:[,.]\d+)?)\s*(ml|unité|unités|portion|paquet)', tail, re.IGNORECASE)
        if not m:
            return ''
        amount = float(m.group(1).replace(',', '.')) * qty
        unit = m.group(2)
        if unit.lower().startswith('unité'):
            unit = 'œuf(s)' if 'œuf' in name.lower() else 'unité(s)'
        elif unit.lower() == 'paquet':
            unit = 'paquet(s)'
        elif unit.lower() == 'portion':
            unit = 'portion(s)'
    shown = f'{amount:.0f}' if abs(amount - round(amount)) < 0.01 else f'{amount:.1f}'
    return f'Quantité utilisée : environ {shown} {unit}'

def custom_inputs(data: dict, prefix: str):
    with ui.grid(columns=5).classes('w-full gap-3 mt-2'):
        ui.input(label='Nom', value=data['name']).on_value_change(lambda e: (data.update({'name': e.value}), refresh()))
        for key, label in [('protein','Protéines g'),('carbs','Glucides g'),('fat','Lipides g'),('kcal','Kcal optionnelles')]:
            ui.number(label=label, value=data[key], min=0, step=1).on_value_change(lambda e, k=key: (data.update({k: float(e.value or 0)}), refresh()))


def add_sport():
    state['sports'].append({'id': str(uuid4()), 'name': "Course 30 min à 6'/km", 'kcal': 250})
    refresh()


def remove_sport(item_id: str):
    state['sports'] = [x for x in state['sports'] if x['id'] != item_id]
    refresh()


def sports_controls():
    ui.separator().classes('my-4')
    with ui.row().classes('items-center justify-between w-full'):
        ui.label('Sports en plus').classes('font-bold text-base')
        ui.button('Ajouter un sport', icon='add', on_click=add_sport).props('unelevated color=primary')
    if not state['sports']:
        ui.label('Ajoute seulement les activités en plus de ta journée choisie. Exemple : une course le soir après une journée muscu.').classes('small mt-1')
        return
    sport_options = [x for x in SPORT_EXTRAS if x != 'Aucun']
    for row in list(state['sports']):
        with ui.row().classes('w-full items-end gap-3 mt-2'):
            ui.select(sport_options, value=row.get('name', sport_options[0]), label='Sport ajouté').on_value_change(lambda e, r=row: (r.update({'name': e.value}), refresh())).classes('grow')
            if row.get('name') == 'Autre sport':
                ui.number(label='Dépense kcal', value=row.get('kcal', 250), min=0, max=2000, step=25).on_value_change(lambda e, r=row: (r.update({'kcal': float(e.value or 0)}), refresh())).classes('w-40')
            extra = sport_row_extra(row)
            ui.label(f'+{extra.energy():.0f} kcal · +{extra.carbs:.0f} g glucides').classes('small mb-3')
            ui.button(icon='delete', on_click=lambda r=row: remove_sport(r['id'])).props('flat round color=negative')


def common_controls():
    profile_card()
    with ui.card().classes('card w-full'):
        ui.label('Réglages du jour').classes('section-title')
        with ui.grid(columns=4).classes('w-full gap-4'):
            ui.select(list(TARGETS), value=state['day'], label='Type de journée').on_value_change(lambda e: setv('day', e.value)).classes('w-full')
            ui.switch('Marche du jour', value=state.get('walk_enabled', True)).on_value_change(lambda e: setv('walk_enabled', e.value)).classes('mt-5')
            ui.number(label='Distance marche en km', value=state.get('walk_km', 4.0), min=0, max=25, step=0.5, format='%.1f').on_value_change(lambda e: setv('walk_km', float(e.value or 0))).classes('w-full')
            ui.number(label='Cafés au lait', value=state['coffee_count'], min=0, max=8, step=1).on_value_change(lambda e: setv('coffee_count', int(e.value or 0))).classes('w-full')
        walk = walking_adjustment()
        sign = '+' if walk.energy() >= 0 else ''
        displayed_walk_km = float(state.get('walk_km') or 0) if state.get('walk_enabled', True) else 0.0
        ui.label(f"Marche : 4 km est le repère de base. Aujourd’hui : {displayed_walk_km:g} km → {sign}{walk.energy():.0f} kcal et {sign}{walk.carbs:.0f} g glucides sur les repères.").classes('small mt-3')
        ui.label(f"Café au lait : {state['coffee_milk_ml']} ml de lait demi-écrémé par café.").classes('small mt-1')
        sports_controls()

def self_controls():
    with ui.card().classes('card w-full'):
        with ui.row().classes('items-center justify-between w-full'):
            ui.label('Self d’entreprise').classes('section-title')
            ui.switch('Je mange au self', value=state['self']).on_value_change(lambda e: setv('self', e.value))
        if state['self']:
            with ui.grid(columns=4).classes('w-full gap-4'):
                ui.select(list(SELF_PROTEINS), value=state['self_protein'], label='Protéine').on_value_change(lambda e: setv('self_protein', e.value))
                ui.select(list(SELF_RICE), value=state['self_rice'], label='Riz').on_value_change(lambda e: setv('self_rice', e.value))
                ui.select(list(SELF_VEG), value=state['self_veg'], label='Légumes').on_value_change(lambda e: setv('self_veg', e.value))
                ui.select(list(SELF_SAUCE), value=state['self_sauce'], label='Sauce').on_value_change(lambda e: setv('self_sauce', e.value))
            ui.html('<div class="box box-info mt-3">Astuce : sauce à part ou petite louche. Si légumes très huileux, garde le dîner plus maigre.</div>')
        ui.label('Autre chose au déjeuner / self').classes('small mt-3')
        custom_inputs(state['self_custom'], 'self_custom')


def add_ingredient(meal: str):
    state['meals'][meal].append({'id': str(uuid4()), 'kind': 'Protéine', 'name': list(PROTEINS)[1], 'qty': 1.0, 'custom': custom_state()})
    refresh()

def remove_ingredient(meal: str, item_id: str):
    state['meals'][meal] = [x for x in state['meals'][meal] if x['id'] != item_id]
    refresh()

def meal_card(title: str):
    with ui.card().classes('card w-full'):
        with ui.row().classes('items-center justify-between w-full'):
            ui.label(title).classes('section-title')
            ui.button('Ajouter un ingrédient', icon='add', on_click=lambda: add_ingredient(title)).props('unelevated color=primary')
        if not state['meals'][title]:
            ui.label('Exemple : filet de poulet + 2 œufs + riz. Les légumes maison restent libres par simplicité.').classes('small')
        for item in list(state['meals'][title]):
            with ui.row().classes('w-full items-end gap-3'):
                def update_kind(e, it=item):
                    it['kind'] = e.value
                    if e.value != 'Autre': it['name'] = ingredient_options(e.value)[1 if e.value != 'Huile / sauce' else 0]
                    refresh()
                ui.select(['Protéine','Féculent','Huile / sauce','Autre'], value=item['kind'], label='Type').on_value_change(update_kind).classes('w-44')
                if item['kind'] == 'Autre':
                    ui.input(label='Nom', value=item['custom']['name']).on_value_change(lambda e, it=item: (it['custom'].update({'name': e.value}), refresh())).classes('w-52')
                    for key, lab in [('protein','Prot. g'),('carbs','Gluc. g'),('fat','Lip. g')]:
                        ui.number(label=lab, value=item['custom'][key], min=0, step=1).on_value_change(lambda e, it=item, k=key: (it['custom'].update({k: float(e.value or 0)}), refresh())).classes('w-28')
                    ui.number(label='Kcal', value=item['custom']['kcal'], min=0, step=10).on_value_change(lambda e, it=item: (it['custom'].update({'kcal': float(e.value or 0)}), refresh())).classes('w-28')
                else:
                    ui.select(ingredient_options(item['kind']), value=item['name'], label='Ingrédient').on_value_change(lambda e, it=item: (it.update({'name': e.value}), refresh())).classes('grow')
                    ui.number(label='Portions', value=item['qty'], min=0, max=8, step=0.25, format='%.2f').on_value_change(lambda e, it=item: (it.update({'qty': float(e.value or 0)}), refresh())).classes('w-32')
                ui.button(icon='delete', on_click=lambda it=item: remove_ingredient(title, it['id'])).props('flat round color=negative')
            if item['kind'] != 'Autre':
                hint = serving_hint(item['name'], float(item.get('qty') or 0))
                if hint:
                    ui.label(hint).classes('small -mt-2 mb-2')
        m = meal_macros(title)
        ui.label(f'Total {title.lower()} : {m.protein:g} g protéines · {m.carbs:g} g glucides · {m.fat:g} g lipides · {m.energy():.0f} kcal').classes('small mt-3')


def extras_card():
    with ui.card().classes('card w-full'):
        ui.label('Petit-déj, goûters et shaker').classes('section-title')
        with ui.grid(columns=2).classes('w-full gap-4'):
            ui.select(list(BREAKFASTS), value=state['breakfast'], label='Petit-déj').on_value_change(lambda e: setv('breakfast', e.value))
            ui.switch('Shaker whey', value=state['shaker']).on_value_change(lambda e: setv('shaker', e.value))
        if state['breakfast'] == 'Autre petit-déj':
            ui.label('Détail autre petit-déj').classes('small mt-3'); custom_inputs(state['breakfast_custom'], 'breakfast_custom')

        ui.separator().classes('my-4')
        with ui.row().classes('items-center justify-between w-full'):
            ui.label('Goûters').classes('font-bold text-base')
            ui.button('Ajouter un goûter', icon='add', on_click=add_snack).props('unelevated color=primary')
        if not state['snacks']:
            ui.label('Exemple : bonbons crocodile + boîte de sushis antigaspi. Ajoute une ligne par goûter mangé.').classes('small mt-1')
        for row in list(state['snacks']):
            with ui.row().classes('w-full items-end gap-3 mt-2'):
                ui.select(list(SNACKS), value=row.get('name', 'Aucun'), label='Goûter').on_value_change(lambda e, r=row: (r.update({'name': e.value}), refresh())).classes('grow')
                if row.get('name') == 'Autre goûter':
                    ui.input(label='Nom', value=row['custom']['name']).on_value_change(lambda e, r=row: (r['custom'].update({'name': e.value}), refresh())).classes('w-52')
                    for key, lab in [('protein','Prot. g'),('carbs','Gluc. g'),('fat','Lip. g')]:
                        ui.number(label=lab, value=row['custom'][key], min=0, step=1).on_value_change(lambda e, r=row, k=key: (r['custom'].update({k: float(e.value or 0)}), refresh())).classes('w-28')
                    ui.number(label='Kcal', value=row['custom']['kcal'], min=0, step=10).on_value_change(lambda e, r=row: (r['custom'].update({'kcal': float(e.value or 0)}), refresh())).classes('w-28')
                else:
                    ui.number(label='Portions', value=row.get('qty', 1.0), min=0, max=8, step=0.25, format='%.2f').on_value_change(lambda e, r=row: (r.update({'qty': float(e.value or 0)}), refresh())).classes('w-32')
                ui.button(icon='delete', on_click=lambda r=row: remove_snack(r['id'])).props('flat round color=negative')
            if row.get('name') != 'Autre goûter':
                hint = serving_hint(row.get('name', ''), float(row.get('qty') or 0))
                if hint:
                    ui.label(hint).classes('small -mt-2 mb-2')
        sm = snack_macros()
        if state['snacks']:
            ui.label(f'Total goûters : {sm.protein:g} g protéines · {sm.carbs:g} g glucides · {sm.fat:g} g lipides · {sm.energy():.0f} kcal').classes('small mt-2')

        ui.separator().classes('my-4')
        if state['shaker']:
            ui.number(label='Lait demi-écrémé dans le shaker en ml', value=state['shaker_ml'], min=0, max=600, step=50).on_value_change(lambda e: setv('shaker_ml', int(e.value or 0))).classes('w-80 mt-3')
            ui.label('Shaker par défaut : 25 g whey + 250 ml lait demi-écrémé. Pas d’autre liquide pour garder la routine stable.').classes('small mt-2')
        ui.label('Autre chose autour du shaker').classes('small mt-3')
        custom_inputs(state['shaker_custom'], 'shaker_custom')

def status_label(st: str) -> str:
    return {'ok':'Dans la zone','warn':'À surveiller','bad':'Hors zone'}[st]

def range_bar(label: str, value: float, center: float, low: float, high: float, unit: str):
    st = status_for(value, low, high)
    max_scale = max(high * 1.35, value * 1.15, 1)
    fill = min(value / max_scale * 100, 100); zone_left = low / max_scale * 100; zone_width = (high - low) / max_scale * 100; mid = center / max_scale * 100
    pill = {'ok':'pill-ok','warn':'pill-warn','bad':'pill-bad'}[st]
    ui.html(f'''
    <div class="range-wrap status-{st}">
      <div class="range-head"><div class="range-title">{label} — {value:.0f} {unit} <span class="pill {pill}">{status_label(st)}</span></div><div class="range-note">zone utile : {low:.0f}-{high:.0f} {unit}</div></div>
      <div class="range-track"><div class="range-zone" style="left:{zone_left:.1f}%;width:{zone_width:.1f}%"></div><div class="range-fill" style="width:{fill:.1f}%"></div><div class="range-mid" style="left:{mid:.1f}%"></div></div>
      <div class="range-labels"><span>0</span><span>repère {center:.0f}</span><span>{max_scale:.0f} {unit}</span></div>
    </div>''')


def dashboard(total: Macros, target: Target):
    ranges = target.ranges()
    statuses = [status_for(total.protein,*ranges['protein']), status_for(total.carbs,*ranges['carbs']), status_for(total.fat,*ranges['fat']), status_for(total.energy(),*ranges['kcal'])]
    overall = 'ok' if all(s == 'ok' for s in statuses) else 'warn' if all(s != 'bad' for s in statuses) else 'bad'
    with ui.card().classes('card w-full'):
        ui.label('Total estimé').classes('section-title')
        ui.html(f'''<div class="metric-grid"><div class="metric"><div class="metric-label">Protéines</div><div class="metric-value">{total.protein:.0f} g</div></div><div class="metric"><div class="metric-label">Glucides</div><div class="metric-value">{total.carbs:.0f} g</div></div><div class="metric"><div class="metric-label">Lipides</div><div class="metric-value">{total.fat:.0f} g</div></div><div class="metric"><div class="metric-label">Énergie</div><div class="metric-value">{total.energy():.0f} kcal</div></div></div>''')
        range_bar('Protéines', total.protein, target.protein, *ranges['protein'], 'g')
        range_bar('Glucides', total.carbs, target.carbs, *ranges['carbs'], 'g')
        range_bar('Lipides', total.fat, target.fat, *ranges['fat'], 'g')
        range_bar('Énergie', total.energy(), target.kcal, *ranges['kcal'], 'kcal')
        box = {'ok':'box-ok','warn':'box-warn','bad':'box-bad'}[overall]
        title = {'ok':'✅ Journée bien calée','warn':'🟡 Journée récupérable','bad':'🔴 Il manque un vrai ajustement'}[overall]
        ui.html(f'<div class="box {box}"><b>{title}</b><br>{dinner_advice(total, target)}</div>')
        ctx = ' '.join([state['self_protein'], state['self_veg'], state['self_sauce']]) if state['self'] else ''
        for w in warnings(total, target, ctx): ui.html(f'<div class="box box-warn">{w}</div>')


def prepare_content():
    ui.html('<div class="hero"><h1 class="h1">Préparer sa journée</h1><div class="subtitle">Planifie tes repas sans tracker compliqué. Les chiffres restent des ordres de grandeur utiles.</div></div>')
    common_controls(); self_controls(); extras_card()
    if not state['self']: meal_card('Déjeuner')
    meal_card('Dîner'); dashboard(total_macros(), current_target())

def completer_content():
    ui.html('<div class="hero"><h1 class="h1">Compléter sa journée</h1><div class="subtitle">Entre ce qui est déjà mangé, puis ajuste le dîner.</div></div>')
    common_controls(); self_controls(); extras_card(); meal_card('Dîner'); dashboard(total_macros(), current_target())
    ui.html('<div class="box box-info"><b>Si faim :</b> ajoute 0,5 portion de féculent ou une banane.<br><b>Version sèche plus agressive :</b> garde protéines/légumes, réduis surtout les glucides hors sport.</div>')

def bilan_content():
    ui.html('<div class="hero"><h1 class="h1">Bilan de journée</h1><div class="subtitle">Regarde si la journée est cohérente, puis exporte si besoin.</div></div>')
    common_controls(); self_controls(); extras_card(); meal_card('Déjeuner'); meal_card('Dîner')
    with ui.card().classes('card w-full'):
        ui.label('Autre aliment de la journée').classes('section-title'); custom_inputs(state['custom'], 'custom')
    total = total_macros(include_custom=True); target = current_target(); dashboard(total, target)
    ui.html(f'<div class="box box-info"><b>Commentaire :</b> {daily_comment(total, target)}<br><b>Suggestion demain :</b> {tomorrow_suggestion(total, target)}</div>')
    with ui.row().classes('mt-4'):
        def export_json():
            path = EXPORT_DIR / f'bilan_{datetime.now():%Y%m%d_%H%M%S}.json'; path.write_text(json.dumps(export_dict(total, target), indent=2, ensure_ascii=False), encoding='utf-8'); ui.notify(f'Export JSON créé : {path.name}')
        def export_csv():
            path = EXPORT_DIR / f'bilan_{datetime.now():%Y%m%d_%H%M%S}.csv'
            with path.open('w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f); writer.writerow(['macro','total','repere']); writer.writerows([['proteines',total.protein,target.protein],['glucides',total.carbs,target.carbs],['lipides',total.fat,target.fat],['kcal',total.energy(),target.kcal]])
            ui.notify(f'Export CSV créé : {path.name}')
        ui.button('Exporter JSON', on_click=export_json).props('unelevated color=primary'); ui.button('Exporter CSV', on_click=export_csv).props('outline color=primary')

@ui.page('/')
def page_prepare(): page_shell('Préparer', prepare_content)
@ui.page('/completer')
def page_completer(): page_shell('Compléter', completer_content)
@ui.page('/bilan')
def page_bilan(): page_shell('Bilan', bilan_content)

ui.run(title='Meal Builder', reload=False)
