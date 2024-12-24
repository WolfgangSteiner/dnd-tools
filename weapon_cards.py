from pdf_tools import Page, Rectangle
from pdf_tools.ornaments import draw_rect_corners_humanized
from types import SimpleNamespace
import re

page = Page("pdf/weapon_cards.pdf", landscape=True)
page.register_font("souvenir/souvenir.ttf", "Souvenir")
page.register_font("souvenir/souvenir_demi.ttf", "SouvenirDemi")
page.register_font("souvenir/souvenir_bold.ttf", "SouvenirBold")
page.register_font("souvenir/souvenir_italic.ttf", "SouvenirItalic")
page.register_font("souvenir/souvenir_bold_italic.ttf", "SouvenirBoldItalic")

_, rects = page.page_rect.apply_margin(10,10).make_grid(44,68)

page.draw_cut_marks(rects)

def to_snake_case(s):
    s = re.sub(r"['()\"]", "", s.lower())
    s = re.sub(r"\s+", "_", s)
    return s


class Weapon:
    def __init__(self, name, attack_dice, attack_modifier=0):
        self.name = name
        self.file_name = to_snake_case(name) + ".png"
        self.attack_modifier = attack_modifier
        self.attack_dice = attack_dice


def draw_equipment_card(page, rect, title, img_filename, text):
    page.push_state()
    page.stroke_width = 1.0
    page.stroke_color = 0.9
    page.font = "SouvenirDemi"
    page.font_size=12
    page.small_caps_factor = 0.65
    gap = 2
    rect = rect.apply_margin(2,2)
    #draw_rect_corners_humanized(page, rect, cfg)
    title_rect, rest = rect.top_partition(height=7.5, gap=gap)
    img_rect, stats_rect = rest.bottom_partition(height=15, gap=gap)

    page.draw_rect_humanized(title_rect)
    page.draw_text_aligned(title, title_rect, small_caps=True)

    page.draw_rect_humanized(img_rect)
    page.draw_image(img_filename, img_rect.apply_margin(2,2))

    page.draw_rect_humanized(stats_rect)
    stats_rect = stats_rect.apply_margin(2,2)
    if text:
        page.layout_text_aligned(text, stats_rect.apply_margin(2,2), font="Souvenir", font_size=10)
    page.pop_state()
    return stats_rect

from character_sheet import draw_field


def draw_hit_field(page, rect, modifier):
    label_rect, value_rect = rect.top_partition(height=3, gap=2)
    page.draw_text_aligned("HIT", label_rect, "center", "top", font="SouvenirDemi", font_size=8)
    page.draw_text_aligned(f"{modifier:+}", value_rect, vertical_align="top", font_size=10) 

def draw_dmg_field(page, rect, weapon, modifier):
    if isinstance(weapon.attack_dice, str):
        attack_dice = (weapon.attack_dice,) 
        font_size = 10
        gap = 2
    else:
        attack_dice = weapon.attack_dice
        font_size = 8
        gap = 1

    label_rect, rect = rect.top_partition(height=3, gap=gap)
    page.draw_text_aligned("DMG", label_rect, "center", "top", font="SouvenirDemi", font_size=8)
     
    for r, atk  in zip(rect.subdivide(len(attack_dice),1), attack_dice):
        page.draw_text_aligned(f"{atk} + {modifier}", r, font_size=font_size, vertical_align="top") 


def draw_weapon_card(page, rect, weapon, ability_modifier=0, proficiency_bonus=0):
    stats_rect = draw_equipment_card(
        page, rect,
        weapon.name,
        f"assets/items/weapons/{weapon.file_name}",
        None)

    page.push_state()
    page.font = "SouvenirDemi"

    hit_rect, dmg_rect = stats_rect.left_partition(0.5)
    draw_hit_field(page, hit_rect, ability_modifier)
    draw_dmg_field(page, dmg_rect, weapon, ability_modifier)
    page.pop_state()



weapons = [
    Weapon("Battle Axe", ("1d8","1d10")),
    Weapon("Quarterstaff", "1d6"),
    Weapon("Longbow", "1d8"),
]
    
num_rects = len(rects)
for i,weapon in enumerate(weapons):
    r = rects[i%num_rects]
    page.draw_rect(r)
    draw_weapon_card(page, r, weapon) 
    if (i + 1) % num_rects == 0:
        page.new_page()


page.save()

