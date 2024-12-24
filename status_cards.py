from pdf_tools import *
from types import SimpleNamespace
import re
import math


def draw_death_card(page, rect):
    rect = rect.apply_margin(5,5)
    page.draw_rect_humanized(rect)
    rect = rect.apply_margin(10,5)
    rects = rect.subdivide(2,3)
    for r in rects[:3]:
        r = r.apply_margin(3,3)
        page.draw_svg("assets/heart.svg", r)
    for r in rects[3:]:
        r = r.apply_margin(1,1)
        page.draw_svg("assets/skull.svg", r)


def rows_for_hearts(hearts):
    if hearts <= 4:
        return 1
    elif hearts == 9:
        return 3
    elif hearts <= 10:
        return 2
    elif hearts <= 15:
        return 3
    else:
        return 4
    
def draw_hp_card_10(page, rect, hearts):
    heart_size = 12 
    heart_rect = Rectangle(0,0,heart_size, heart_size)
    page.draw_rect(rect)
    rect = rect.apply_margin(5,5)
    for i, row in enumerate(rect.subdivide(3, 1)):
        for r in row.subdivide(1, 2 if i == 1 else 4):
            r = heart_rect.align_to_rect(r)
            page.draw_svg("assets/heart.svg", r)

        

def draw_hp_card(page, rect, hearts):
    heart_size = 15 if hearts <= 6 else 10
    heart_rect = Rectangle(0,0,heart_size, heart_size)

    page.draw_rect(rect)
    rect = rect.apply_margin(5,5)
    num_rows = rows_for_hearts(hearts)
    hearts_per_row = math.ceil(hearts / num_rows)
    for i, row in enumerate(rect.subdivide(num_rows, 1)):
        hearts_in_row = min(hearts, hearts_per_row)
        for r in row.subdivide(1, hearts_per_row):
            r = r.apply_margin(2,2)
            r = heart_rect.align_to_rect(r)
            page.draw_svg("assets/heart.svg", r)
            hearts -= 1
            if hearts == 0:
                break

def draw_hp_card_numbered(page, rect, hearts):
    rect = rect.apply_margin(5,5)
    w = rect.w / 10
    count = 0 
    num_rows = math.floor(rect.h / w)
    for r in rect.subdivide(num_rows, 10):
        page.draw_rect(r)
        page.draw_text_centered(r, str(count))
        count += 1



def draw_ammo_block(page, rect):
    gap = 2
    radius = 2
    bbox = Rectangle(0, 0, 10*radius + 4 * gap, 2*radius)
    bbox = bbox.align_to_rect(rect)
    for r in bbox.subdivide(1, 5, horizontal_gap=gap):
        page.draw_rect(r, radius=radius, stroke_width=1)


def draw_ammo_field(page, rect):
    page.draw_rect(rect, radius=2, stroke_width=1)
    rect = rect.apply_margin(2, 2)
    page.draw_text_aligned("Ammunition", rect, vertical_align="bottom", horizontal_align="right")
    rect = rect.apply_margin_right(20)
    for r in rect.subdivide(2, 2):
        draw_ammo_block(page, r)


def draw_hp_card_pencil(page, rect):
    rect = rect.apply_margin(5,5)
    rows = rect.subdivide([1,2,1], 1, vertical_gap=2)

    stat_row, hp_row, ammo_row = rows
    draw_fields(page, stat_row, ["INI", "AC", "Attacks"])
    draw_fields(page, hp_row, ["Total HP", "Current HP", "Temp HP"])
    draw_ammo_field(page, ammo_row)


ABILITIES = ('str', 'dex', 'con', 'int', "wis", "cha")


def id_for_label(label):
    id = re.sub("['\"*+~()\[\]\{\}]", "", label.lower())
    return id

def format_modifier(page, modifier, rect, font=None, font_size=None):
    bbox = page.text_bounding_box(str(abs(modifier)), font=font, font_size=font_size)
    bbox = bbox.align_to_rect(rect)
    page.draw_text(bbox.pos, str(abs(modifier)), font=font, font_size=font_size)
    sign = "+" if modifier > 0 else "-" if modifier < 0 else ""
    bbox_sign = page.text_bounding_box(sign, font=font, font_size=font_size)
    y_offset = 0.5 if modifier > 0 else 0
    offset = Point(-bbox_sign.w, y_offset)
    page.draw_text(bbox.pos + offset, sign, font=font, font_size=font_size)


def draw_field(page, rect, text, values=SimpleNamespace(), humanized=False, draw_frame=True):
    page.font = "SouvenirDemi"
    page.stroke_width = 0.4 
    page.stroke_color = 0

    if draw_frame:
        if humanized:
            page.draw_rect_humanized(rect, stroke_width=0.4, curvature_spread=0.2, point_spread=0.25, num_strokes=2)
        else:
            page.draw_rect(rect, radius=2, stroke_width=1)

    id = id_for_label(text)
    value = getattr(values, id, "")

    top_row, value_box = rect.top_partition(height=4)
    label_rect, label_align = top_row, "center"
    value_box = rect
    if text.lower() in ABILITIES: 
        _, prof_box = top_row.right_partition(width=4)
        label_align = "left"
        page.draw_text_aligned(text, label_rect.apply_margin(1,0), "left", "center", font_size=10)
        page.draw_line_humanized(prof_box.left_edge()) 
        page.draw_line_humanized(prof_box.bottom_edge()) 
        if value:
            modifier = int((value - 10) / 2)
            mod_str = f"{modifier:+}"
             
            format_modifier(page, modifier, value_box, font="SouvenirDemi", font_size=16)
            page.draw_text_aligned(str(value), rect.apply_margin(1,1), font="Souvenir", font_size=8, horizontal_align="right", vertical_align="bottom")
        #page.draw_line_humanized(prof_box.bottom_edge()) 

    elif text:
        page.draw_text_aligned(text, label_rect, horizontal_align=label_align, vertical_align="center")
        if value:
            page.draw_text_aligned(str(value), value_box, font_size=16)
        #page.draw_line_humanized(top_row.bottom_edge())

def draw_fields(page, rect, labels, values=SimpleNamespace(), humanized=False):
    for i,r in enumerate(rect.subdivide(1, len(labels), horizontal_gap=2)):
        draw_field(page, r, labels[i], values=values, humanized=humanized)


def draw_ability_fields(page, rect, values=SimpleNamespace(), humanized=True):
    ability_labels = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
    draw_fields(page, rect, ability_labels, values=stats, humanized=True)

def ancestry_adjective(ancestry):
    adjectives = {'dwarf':'dwarven', 'elf': 'elvish', 'half-elf': 'half-elf'}
    return adjectives.get(ancestry.lower(), ancestry)

def get_ability_modifier(stats, ability):
    value = getattr(stats, ability)
    return int((value - 10)/2)

def draw_name_exp_fields(page, rect, values=SimpleNamespace(), humanized=True):
    draw_field(page, rect, "", humanized=humanized)
    left_field,lvl_field = rect.right_partition(width=16)
    page.draw_line_humanized(lvl_field.left_edge())
    draw_field(page, lvl_field, "EXP", values=stats, draw_frame=False) 
    name_field, type_field = left_field.top_partition(0.6)
    page.draw_text_aligned(values.name, name_field, font_size=14)
    type_str = f"{ancestry_adjective(values.ancestry).capitalize()} {values.profession} (lvl {values.level})"
    page.draw_text_aligned(type_str, type_field, font_size=10, vertical_align="top")


def sort_skills(skills):
    skills = sorted(skills)
    sorted_skills = []
    for ability in ABILITIES:
        for skill in skills:
            if ability_for_skill(skill) == ability:
                sorted_skills.append(skill)
    return sorted_skills


def draw_skills(page, rect, values=SimpleNamespace(), num_rows=8, humanized=True):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    page.draw_text_aligned("Skills", rect.apply_margin(1,1), "left", "top", font_size=10)
    rows = rect.apply_margin(2,2).subdivide(num_rows, 1)
    if not hasattr(values, "skills"):
        return
    for i,skill in enumerate(sort_skills(values.skills)):
        skill_str = skill.capitalize()
        ability = ability_for_skill(skill)
        ability_modifier = get_ability_modifier(values, ability)
        skill_modifier = ability_modifier + values.proficiency_bonus
        skill_str = f"{skill_str} ({skill_modifier:+})"
        color = 1.0 if i % 2 else 0.8
        page.draw_line_humanized(rows[i].bottom_edge(), stroke_width=0.4)
        page.draw_text_aligned(skill_str, rows[i], "left", "center")


def draw_attacks(page, rect, values=SimpleNamespace(), num_rows=8, humanized=True):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    page.draw_text_aligned("Attacks", rect.apply_margin(1,1), "left", "top", font_size=10)

def draw_character_sheet_a5(page, rect, stats=SimpleNamespace(), humanized=True):
    page.font = "SouvenirDemi"
    page.stroke_width = 0.4 
    page.stroke_color = 0
    gap = 2

    rect = rect.apply_margin(10,10)
    ability_row, rect = rect.top_partition(height=16.0)
    ability_rect, name_rect = ability_row.left_partition(0.6, gap=2)
    draw_ability_fields(page, ability_rect, values=stats, humanized=humanized)
    draw_name_exp_fields(page, name_rect, values=stats, humanized=humanized)

    rect.h -= gap
    skill_rect, attack_rect = rect.right_partition(width=name_rect.w)[1].top_partition(0.5, gap=gap)
    draw_skills(page, skill_rect, values=stats)
    draw_attacks(page, attack_rect, values=stats)

    #p.draw_humanized_rect(rect.apply_margin(5, 5), stroke_width=1.0, stroke_color=0, curvature_spread=0.2, point_spread=0.5, num_strokes=2)

def ability_for_skill(skill):
    skills = {"athletics": "str", "intimidation":"cha", "perception":"wis", "survival":"wis"}
    return skills[skill.lower()]


page = Page("pdf/status_cards.pdf", landscape=True)
page.register_font("souvenir/souvenir.ttf", "Souvenir")
page.register_font("souvenir/souvenir_demi.ttf", "SouvenirDemi")
page.register_font("souvenir/souvenir_bold.ttf", "SouvenirBold")
page.register_font("souvenir/souvenir_italic.ttf", "SouvenirItalic")
page.register_font("souvenir/souvenir_bold_italic.ttf", "SouvenirBoldItalic")

for r in page.subdivide(4,4):
    draw_death_card(page, r)

page.new_page(landscape=False)

stats = SimpleNamespace(str=16, dex=14, con=16, int=10, wis=10, cha=10, level=2, name="Orikour", ancestry="Dwarf", profession="Barbarian", proficiency_bonus=2, skills=["athletics", "intimidation", "perception", "survival"])

for r in page.subdivide(2, 1):
    draw_character_sheet_a5(page, r, stats)

#hearts_arr = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 16] 

#for i, hearts in enumerate(hearts_arr):
#    r = rects[i]
#    draw_hp_card_numbered(p, r, hearts)
        

page.save()
