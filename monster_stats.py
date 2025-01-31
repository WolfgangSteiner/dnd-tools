from pdf_tools import Page, Rectangle, Line
from dnd_tools import Monster
import typer

def capitalize_words(text):
    return " ".join([word.capitalize() for word in text.split()])

def draw_field(page, rect, title, values, draw_box=False, mod=False, right_to_left=False):
    if title.startswith("+"):
        mod = True
        title = title[1:]

    if ":" in title:
        title, key = title.split(":")
    else:
        key = title

    value = values[key]

    if mod:
        value = f"{value:+}"

    if draw_box:
        page.draw_rect_humanized(rect, stroke_width=0.4, stroke_color=0)
        label_horizontal_align = "left"
    else:
        label_horizontal_align = "center"
        
    body = rect.apply_margin(1,1)
    page.draw_text_aligned(title, body, label_horizontal_align, "top", font="SouvenirBold", font_size=8, small_caps=True)
    page.draw_text_aligned(value, body, "center", "bottom", font="SouvenirBold", font_size=10)

    if right_to_left:
        return rect.duplicate_left(gap=2)
    else:
        return rect.duplicate_right(gap=2)

def draw_stat(page, rect, title, value):
    page.draw_text_aligned(f"{title} {value}", rect, font="SouvenirBold", font_size=10, small_caps=True)
    return rect.duplicate_right(gap=2)


def draw_heading(page, rect, monster):
    gap = 2
    bbox = page.draw_text_aligned(capitalize_words(monster.name), rect.apply_margin(x=gap), font="SouvenirBold", font_size=12, small_caps=True, horizontal_align="left", vertical_align="top")
    bbox = bbox.union(page.draw_text_aligned(f" {monster.size} {monster.type}", bbox, "left", "below", font="SouvenirBold", font_size=10, small_caps=True, vertical_gap=2))
    rect, remain = rect.top_partition(height=bbox.h)
    rect = rect.apply_margin(x=gap)
    stat_rect = rect.bottom_right_rectangle(6, 6)
    for stat in ["hp", "ac", "+ini", "per:passive_perception"]:
        stat_rect = draw_field(page, stat_rect, stat, monster.as_dict, draw_box=False, right_to_left=True)

    return remain

def draw_separator(page, rect, title=""):
    margin=2
    if title:
        titlebox, rect = rect.top_partition(height=5)
        titlebox = titlebox.apply_margin(x=margin)
        page.draw_text_aligned(title, titlebox, "left", "bottom", font="SouvenirBold", small_caps=True)
    rect, remain = rect.top_partition(height=2)
    rect = rect.apply_margin(x=margin)
    line = Line(rect.left_center(), rect.right_center())
    page.draw_line_humanized(line, stroke_width=0.5, stroke_color=0.0)
    return remain


def draw_abilities_stats(page, rect, monster):
    rect = draw_separator(page, rect)
    field_width = 6
    gap = 2
    rect, remain = rect.top_partition(height=field_width)
    rect = rect.apply_margin(gap,0)
    ability_rect,_ = rect.left_partition(width=field_width)
    for ability in monster.abilities:
        ability_rect = draw_field(page, ability_rect, ability, monster.abilities, mod=True)

    stats_rect = Rectangle(w=2*field_width + gap).align_to_rect(rect, "right", "block")
    stats_rect.w = field_width
    for stat in ("cr", "xp"):
        stats_rect = draw_field(page, stats_rect, stat, monster.as_dict)


    return remain

def get_action_text(action):
    text = f"<b><i>{capitalize_words(action['name'])}.</i></b>"
    
    if "atk" in action:
        text += f" ATK {action['atk']:+}, DMG {action['dmg']}"

    return text


def format_item(item):
    if isinstance(item, list) or isinstance(item, tuple):
        title, text = item
        return f"<b><i>{capitalize_words(title)}.</i></b> {text}"
    else:
        return capitalize_words(item)


def draw_list(page, rect, monster, title, items, format_func=format_item):
    if items:
        rect = draw_separator(page, rect, title)
        for item in items:
            textbox = rect.apply_margin(x=2)
            text = format_func(item) 
            bbox = page.layout_text_aligned(text, textbox, font_size=8, font="RobotoSlab", horizontal_align="left", vertical_align="top", auto_fit=False)
            _, rect = rect.top_partition(height=bbox.h, gap=1)
    return rect


def build_specials_text(monster):
    text_arr = []
    for special in monster.specials:
        if isinstance(special, str):
            text_arr.append(capitalize_words(special))
        else:
            text_arr.append(f"{capitalize_words(special[0])} ({special[1]})")
    return ", ".join(text_arr)


def draw_monster_stat(page, rect, monster):
    x1, y2 = rect.x1, rect.y2
    gap = 2
    rect = rect.apply_margin(x=gap,top=gap*2,bottom=gap)
    rect = draw_heading(page, rect, monster)
    rect = draw_list(page, rect, monster, "Actions", monster.actions, get_action_text)
    rect = draw_list(page, rect, monster, "Bonus Actions", monster.bonus_actions)
    rect = draw_list(page, rect, monster, "Reactions", monster.reactions)

    specials = [("Specials", build_specials_text(monster))]
    if monster.immunities:
        immunities = ", ".join([capitalize_words(item) for item in monster.immunities])
        specials.append(("Immunities", immunities))
    if monster.resistances:
        resistances = ", ".join([capitalize_words(item) for item in monster.resistances])
        specials.append(("Resistances", resistances))
    rect = draw_list(page, rect, monster, "", specials)
    rect = draw_abilities_stats(page, rect, monster)
    bbox = Rectangle(x1, rect.y2 - gap, rect.w + 2*gap, y2 - rect.y2 + gap)
    page.draw_rect_humanized(bbox, stroke_width=0.4, stroke_color=0)
    return bbox


def main():
    page = Page(landscape=True)
    monsters = Monster.load_monsters_from_directory("monsters")
    rects = page.page_rect.apply_margin(20,20).subdivide(2, 3, horizontal_gap=2, vertical_gap=5, col_wise=True)
    rects_per_page = 6

    for i, monster_name in enumerate(sorted(monsters.keys())):
        bbox = draw_monster_stat(page, rects[i%rects_per_page], monsters[monster_name])
        if i == rects_per_page - 1:
            page.new_page()


    page.save()


if __name__ == "__main__":
    typer.run(main)
