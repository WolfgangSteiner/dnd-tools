from pdf_tools import *
from types import SimpleNamespace
import re
import math
from dnd_tools.dnd_character import Character, ability_for_skill, sort_skills, ABILITIES
from pygrv import get_arg

def id_for_label(label):
    id = re.sub("['\"*+~()\[\]\{\}]", "", label.lower())
    id = id.replace(" ", "_")
    return id

def snake_case_to_capitalized_words(string):
    words = string.split("_")
    capitalized_words = [word.capitalize() for word in words]
    return " ".join(capitalized_words)


def format_modifier(page, modifier, rect, font=None, font_size=None):
    bbox = page.text_bounding_box(str(abs(modifier)), font=font, font_size=font_size)
    bbox = bbox.align_to_rect(rect)
    page.draw_text(bbox.pos, str(abs(modifier)), font=font, font_size=font_size)
    sign = "+" if modifier > 0 else "-" if modifier < 0 else ""
    bbox_sign = page.text_bounding_box(sign, font=font, font_size=font_size)
    y_offset = 0.5 if modifier > 0 else 0
    offset = Point(-bbox_sign.w, y_offset)
    page.draw_text(bbox.pos + offset, sign, font=font, font_size=font_size)


def draw_field(page, rect, label, values=SimpleNamespace(), value=None, humanized=False, draw_frame=True, is_modifier=False, small_caps=True):
    page.font = "SouvenirDemi"
    page.stroke_width = 0.4 
    page.stroke_color = 0
    if ":" in label:
        label, id = label.split(":=")
    else:
        id = id_for_label(label)

    if draw_frame:
        if humanized:
            page.draw_rect_humanized(rect, stroke_width=0.4, curvature_spread=0.2, point_spread=0.25, num_strokes=2)
        else:
            page.draw_rect(rect, radius=2, stroke_width=1)


    if value is None:
        value = getattr(values, id, "")

    top_row, value_box = rect.top_partition(height=4)
    label_rect, label_align = top_row, "left"
    value_box = rect
    value_font_size = 16 if len(str(value)) < 3 else 12
    if label.lower() in ABILITIES:
        ability = label.lower()
        _, prof_box = top_row.right_partition(width=6)
        label_align = "left"
        page.draw_text_aligned(label, label_rect.apply_margin(1,1), "left", "top", font_size=8, small_caps=small_caps)
        saving_throws = getattr(values, "saving_throws", [])
        has_saving_throw = ability in saving_throws

        if False and has_saving_throw:
            page.fill_rect(prof_box.apply_margin(0.75,0.75), fill_color=0.2)
        page.draw_line_humanized(prof_box.left_edge()) 
        page.draw_line_humanized(prof_box.bottom_edge()) 

        if value:
            modifier = int((value - 10) / 2)
            saving_throw_modifier = modifier
            if has_saving_throw:
                saving_throw_modifier += getattr(values, "proficiency_bonus", 0)
            page.draw_text_aligned(f"{saving_throw_modifier:+}", prof_box, font="SouvenirDemi", font_size=8)

            mod_str = f"{modifier:+}"
            format_modifier(page, modifier, value_box, font=page.font, font_size=value_font_size)
            page.draw_text_aligned(str(value), rect.apply_margin(1,1), font="Souvenir", font_size=8, horizontal_align="right", vertical_align="bottom")
        #page.draw_line_humanized(prof_box.bottom_edge()) 

    elif label:
        page.draw_text_aligned(label, label_rect.apply_margin(1,1), horizontal_align=label_align, vertical_align="top", small_caps=small_caps, font_size=8)
        if label.lower() == 'spd':
            page.draw_text_aligned(f"{value}ft", value_box.apply_margin(1,1), "right", "bottom", font="Souvenir", font_size=8)
            value = value // 5
        if value:
            value_str = f"{value:+}" if is_modifier else str(value)
            page.draw_text_aligned(value_str, value_box, font_size=value_font_size)
        #page.draw_line_humanized(top_row.bottom_edge())

def draw_text_field(page, rect, title, values=SimpleNamespace(), value=None, humanized=False, draw_frame=True, small_caps=True):
    page.font = "SouvenirDemi"
    page.stroke_width = 0.4 
    page.stroke_color = 0

    if draw_frame:
        if humanized:
            page.draw_rect_humanized(rect, stroke_width=0.4, curvature_spread=0.2, point_spread=0.25, num_strokes=2)
        else:
            page.draw_rect(rect, radius=2, stroke_width=1)

    id = id_for_label(title)

    if value is None:
        value = getattr(values, id, "")

    top_row, value_box = rect.top_partition(height=4)
    label_rect, label_align = top_row, "left"
    value_box = rect
    value_font_size = 16 if len(str(value)) < 3 else 12
    if title:
        page.draw_text_aligned(title, label_rect.apply_margin(1,1), horizontal_align=label_align, vertical_align="top", small_caps=small_caps, font_size=8)
        if value:
            page.draw_text_aligned(value, value_box, font_size=value_font_size)


def draw_fields(page, rect, labels, values=SimpleNamespace(), humanized=False, num_rows=1, num_cols=None):
    num_cols = get_arg(num_cols, len(labels))
    for i,r in enumerate(rect.subdivide(num_rows, num_cols, horizontal_gap=2, vertical_gap=2)):
        label = labels[i]
        is_modifier = label.startswith('+')
        if is_modifier:
            label = label[1:]

        draw_field(page, r, label, values=values, humanized=humanized, is_modifier=is_modifier)


def draw_hp_field(page, rect, character):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    max_hp_rect, cur_hp_rect, tmp_hp_rect = rect.subdivide(1, 3)
    page.draw_text_aligned("HP", max_hp_rect.apply_margin(0,1), vertical_align="top", font_size=8, small_caps=True)
    page.draw_text_aligned(str(character.max_hp), max_hp_rect, font_size=14)
    page.draw_text_aligned("Cur", cur_hp_rect.apply_margin(0,1), vertical_align="top", font_size=8, small_caps=True)
    page.draw_text_aligned("Tmp", tmp_hp_rect.apply_margin(0,1), vertical_align="top", font_size=8, small_caps=True)
    page.draw_svg("assets/heart2.svg", cur_hp_rect.apply_margin(2,2), stroke_color=0.75)

def draw_coins_field(page, rect, character):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    gold_rect, silver_rect  = rect.subdivide(2, 1)
    page.draw_line_humanized(gold_rect.apply_margin(0, 0).bottom_edge(), stroke_width=0.4) 
    page.draw_text_aligned("gp", gold_rect.apply_margin(1,1), horizontal_align="left", vertical_align="top", font_size=8, small_caps=True)
    page.draw_text_aligned("sp", silver_rect.apply_margin(1,1), horizontal_align="left", vertical_align="top", font_size=8, small_caps=True)

def draw_ability_fields(page, rect, values=SimpleNamespace(), humanized=True, num_rows=1, num_cols=6):
    ability_labels = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
    draw_fields(page, rect, ability_labels, values=values, humanized=True, num_rows=num_rows, num_cols=num_cols)


def ancestry_adjective(ancestry):
    adjectives = {'dwarf':'dwarven', 'elf': 'elvish', 'half-elf': 'half-elf'}
    return adjectives.get(ancestry.lower(), ancestry)


def get_ability_modifier(stats, ability):
    value = getattr(stats, ability)
    return int((value - 10)/2)

def capitalize_words(string):
    return " ".join([w.capitalize() for w in string.split()])


def draw_name_exp_fields(page, rect, values=SimpleNamespace(), humanized=True):
    draw_field(page, rect, "", humanized=humanized)
    left_field,lvl_field = rect.right_partition(width=16)
    page.draw_line_humanized(lvl_field.left_edge())
    draw_field(page, lvl_field, "XP", values=values, draw_frame=False) 
    name_field, type_field = left_field.top_partition(0.6)
    page.draw_text_aligned(values.name, name_field, font_size=14, small_caps=True)
    ancestry = capitalize_words(ancestry_adjective(values.ancestry))
    type_str = f"Lvl {values.level} {ancestry} {values.profession}"
    page.draw_text_aligned(type_str, type_field, font_size=9, vertical_align="top", small_caps=True)

def draw_skills(page, rect, values=SimpleNamespace(), num_rows=8, humanized=True, heading=True):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    header, body = rect.apply_margin(0,0).top_partition(height=7)
    header, pb_field = header.left_partition(width=20)
    pb_label_rect, pb_value_rect = pb_field.right_partition(width=11)
    page.draw_text_aligned("Prof. Bonus", pb_label_rect.apply_margin(2,2), "left", "center", small_caps=True)
    page.draw_text_aligned(f"{values.proficiency_bonus:+}", pb_value_rect.apply_margin(4,2), "right", "center")
    page.draw_line_humanized(pb_field.bottom_edge(), stroke_width=0.4)
    page.draw_line_humanized(pb_field.left_edge(), stroke_width=0.4)
    #page.draw_line_humanized(pb_value_rect.left_edge(), stroke_width=0.4)
    page.draw_text_aligned("Skills", header.apply_margin(4,2), "left", "center", font_size=10, small_caps=True)
    rows = body.apply_margin(2,0).subdivide(num_rows, 1)
    if not hasattr(values, "skills"):
        return
    for i,skill in enumerate(sort_skills(values.skills)):
        row = rows[i]
        skill_field, modifier_field = row.apply_margin(2,0).right_partition(width=5)
        skill_str = snake_case_to_capitalized_words(skill)
        ability = ability_for_skill(skill)
        ability_modifier = get_ability_modifier(values, ability)
        skill_modifier = ability_modifier + values.proficiency_bonus
        page.draw_line_humanized(rows[i].bottom_edge(), stroke_width=0.4)
        page.draw_text_aligned(skill_str, skill_field, "left", "center", small_caps=True)
        page.draw_text_aligned(f"{skill_modifier:+}", modifier_field, "right", "center")



def draw_list_row(page, rect, item, subdivide_factors=None, align=None, margin=2, draw_separator=True):
    col_items = item.split("|")
    subdivide_factors = get_arg(subdivide_factors, [1/len(col_items) for i in col_items])    
    col_aligns = align.split("|") if align is not None else ["l" for i in col_items]
    row_rect = rect.apply_margin(margin,0)
    content_rect = rect.apply_margin(2 * margin,0)
    for r, col_text, col_align in zip(content_rect.subdivide(1, subdivide_factors), col_items, col_aligns):
        page.draw_text_aligned(col_text, r, col_align, small_caps=True)
    if draw_separator:
        page.draw_line_humanized(row_rect.bottom_edge(), stroke_width=0.4)
         

def draw_list(page, rect, title, items, num_rows, num_cols, subdivide_factors=None, align=None, heading=True):
    if heading:
        header, rect = rect.apply_margin(0,0).top_partition(height=7)
        draw_list_row(page, header, title, subdivide_factors, align, draw_separator=False)
    rows = rect.subdivide(num_rows, 1)
    for i,item in enumerate(items):
        col_items = item.split("|")
        row = rows[i]
        draw_list_row(page, row, item, subdivide_factors, align, draw_separator=(i!=len(items)-1))


def draw_attacks(page, rect, values=SimpleNamespace(), num_rows=7, humanized=True, gap=2, heading=True):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    draw_list(page, rect, "Attack|Hit|Dmg", values.attacks, num_rows, 3, (0.5,0.2, 0.3), align="l|r|r") 


def draw_other_stats_fields(page, rect, values=SimpleNamespace(), humanized=True, gap=2):
    draw_fields(page, rect, ("AC", "+INI", "SPD", "Pass Per:=passive_perception", "Hit Dice", ""), values=values, humanized=True)


def draw_proficiency_field(page,rect, character=SimpleNamespace(), humanized=True, gap=2, heading=True):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    draw_list(page, rect, "Proficiencies", character.proficiencies, num_rows=8, num_cols=1, heading=heading)


def draw_feats_traits(page,rect, character=SimpleNamespace(), humanized=True, gap=2, heading=True):
    page.draw_rect_humanized(rect, stroke_width=0.4)
    draw_list(page, rect, "Feats & Traits", character.feats_traits, num_rows=8, num_cols=1, heading=heading)


def draw_character_sheet_a5(page, rect, character=SimpleNamespace(), humanized=True):
    page.font = "SouvenirDemi"
    page.stroke_width = 0.4 
    page.stroke_color = 0
    gap = 2

    rect = rect.apply_margin(10,10)
    ability_row, _ = rect.top_partition(height=16.0, gap=gap)

    ability_rect, name_rect = ability_row.left_partition(0.6, gap=2)
    column_width = (ability_rect.w - gap) / 2
    first_column = Rectangle(rect.x1, rect.y1, column_width, rect.h)
    second_column = first_column.horizontal_align_to_rect(first_column, "right_of", gap)
    third_column = Rectangle(name_rect.x1, rect.y1, name_rect.w, rect.h)

    draw_ability_fields(page, ability_rect, values=character, humanized=humanized)
    draw_name_exp_fields(page, name_rect, values=character, humanized=humanized)

    other_stats_rect = Rectangle(h=16).horizontal_align_to_rect(first_column.union(second_column), "block").vertical_align_to_rect(ability_rect, "below", gap=2)

    hp_rect = Rectangle(h=16).horizontal_align_to_rect(second_column, "block").vertical_align_to_rect(ability_rect, "below", gap=2)

    attack_rect = Rectangle(h=60).horizontal_align_to_rect(first_column, "block").vertical_align_to_rect(other_stats_rect, "below", gap=2)

    if character.is_spellcaster:
        spell_slots_rect = Rectangle(x1=rect.x1, x2=ability_rect.x2, h=10).vertical_align_to_rect(other_stats_rect, "below", gap)
        attack_rect = attack_rect.vertical_align_to_rect(spell_slots_rect, "below", gap)
        draw_spell_slots(page, spell_slots_rect, character)

    skill_rect = attack_rect.duplicate_right(gap)
    proficiency_rect = attack_rect.duplicate_below(gap)
    feats_traits_rect = proficiency_rect.duplicate_right(gap)

    hp_rect = Rectangle(w=name_rect.w/2).horizontal_align_to_rect(name_rect, "left").vertical_align_to_rect(other_stats_rect, "block")

    draw_other_stats_fields(page, other_stats_rect, values=character)
    draw_hp_field(page, hp_rect, character=character)

    draw_coins_field(page, Rectangle(w=16,h=16).align_to_rect(name_rect, horizontal_align="right", vertical_align="below", vertical_gap=gap), character)

    draw_skills(page, skill_rect, values=character)
    draw_attacks(page, attack_rect, values=character)
    draw_proficiency_field(page, proficiency_rect, character=character)
    draw_feats_traits(page, feats_traits_rect, character)

    spell_slots_width = 10
    inventory_rect = Rectangle(x1=name_rect.x1, x2=name_rect.x2).vertical_align_to_rect(skill_rect, "block")

    draw_inventory(page, inventory_rect, character)

    text_rect = Rectangle(y1=proficiency_rect.y1, y2=proficiency_rect.y2).horizontal_align_to_rect(name_rect, "block")
    draw_personality(page, text_rect, character, gap=gap)


def draw_inventory(page, rect, character, heading=False, gap=2):
    draw_text_field(page, rect, "Gear", humanized=True)
    for i,r in enumerate(rect.apply_margin(2,2).subdivide(10,2, horizontal_gap=2, col_wise=True)):
        page.draw_text_aligned(f"{i+1:2d}", r.apply_margin(0,1), horizontal_align="left", vertical_align="bottom", font="Souvenir", font_size=6) 
        page.draw_line(r.bottom_edge(), stroke_width=0.5)
    
def draw_spell_slots(page, rect, character, gap=2):
    spell_levels = ["1st", "2nd", "3rd"] + [f"{i}th" for i in range(2,10)]
    draw_fields(page, rect, spell_levels, humanized=True) 

def draw_personality(page, rect, character, heading=False, gap=2):
    text_rects = rect.subdivide(4,1, vertical_gap=gap)
    for title, text_rect in zip(("Personality", "Ideals", "Bonds", "Flaws"), text_rects):
        draw_text_field(page, text_rect, title, humanized=True)

    #p.draw_humanized_rect(rect.apply_margin(5, 5), stroke_width=1.0, stroke_color=0, curvature_spread=0.2, point_spread=0.5, num_strokes=2)

def draw_character_sheet_a6(page, rect, character=SimpleNamespace(), humanized=True):
    page.font = "SouvenirDemi"
    page.stroke_width = 0.4 
    page.stroke_color = 0
    gap = 2

    rect = rect.apply_margin(5,5)
    raster_w = 17
    raster_h = 16
    header_row, body = rect.top_partition(height=raster_h, gap=gap)
    ability_rect = Rectangle(rect.x1, 0, 2*raster_w+gap, 3*raster_h+2*gap).vertical_align_to_rect(body, "top")
    draw_name_exp_fields(page, header_row, values=character, humanized=humanized)
    draw_ability_fields(page, ability_rect, num_rows=3, num_cols=2, values=character, humanized=humanized)

    #draw_ac_ini_spd_fields(page, other_stats_rect, values=character)
    #draw_hp_fields(page, hp_rect, values=character)


def draw_character_sheet_card(page, rect, character, title, draw_func, gap=2):
    body = rect.apply_margin(5,5)
    header, body = body.top_partition(height=13, gap=gap)
    page.draw_rect_humanized(header, stroke_width=0.4)
    name_rect, title_rect = header.apply_margin(2,2).top_partition(0.6) 
    page.draw_text_aligned(character.name, name_rect, small_caps=True, font_size=14, vertical_align="center")
    page.draw_text_aligned(title, title_rect, small_caps=True, font_size=12)
    draw_func(page, body, character, heading=False) 

def draw_character_sheet_cards(page, rect, character):
    rects = rect.subdivide(2,4)
    char_sheet_rect = rects[0].union(rects[1])
    rects = rects[2:]
    draw_character_sheet_a6(page, char_sheet_rect, character)
    for i, (title, draw_func) in enumerate([
        ("Proficiencies", draw_proficiency_field),
        ("Skills", draw_skills),
        ("Attacks", draw_attacks),
        ("Feats & Traits", draw_feats_traits),
        ("Personality", draw_personality),
        ("Inventory", draw_inventory),
    ]):
        draw_character_sheet_card(page, rects[i], character, title, draw_func)


def main():
    page = Page("pdf/character_sheet.pdf", pagesize=Page.A4, landscape=False)
    page.register_font("souvenir/souvenir.ttf", "Souvenir")
    page.register_font("souvenir/souvenir_demi.ttf", "SouvenirDemi")
    page.register_font("souvenir/souvenir_bold.ttf", "SouvenirBold")
    page.register_font("souvenir/souvenir_italic.ttf", "SouvenirItalic")
    page.register_font("souvenir/souvenir_bold_italic.ttf", "SouvenirBoldItalic")
    page.register_font("roboto_slab/roboto_slab_bold.ttf", "RobotoSlabBold")
    page.register_font("roboto_slab/roboto_slab_semibold.ttf", "RobotoSlabSemiBold")
    page.register_font("roboto_slab/roboto_slab_regular.ttf", "RobotoSlab")

    from orikour import orikour
    from tombur import tombur

    characters = [tombur, orikour]

    
    for character in characters:
        draw_character_sheet_a5(page, page.page_rect, character)
        page.new_page(landscape=True)
        draw_character_sheet_cards(page, page.page_rect, character)
        page.new_page(landscape=False)
    #hearts_arr = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 16] 

    #for i, hearts in enumerate(hearts_arr):
    #    r = rects[i]
    #    draw_hp_card_numbered(p, r, hearts)
            

    page.save()


if __name__ == "__main__":
    main()
