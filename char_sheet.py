from reportlab.lib.pagesizes import A6, landscape
from reportlab.pdfgen import canvas
from pdf_tools import Page, Rectangle, Point, Line

def draw_ability_field(page, pos, ability, proficiencies, width=22, height=20, radius=1.0):
    page.stroke_width = 1.0
    page.stroke_color = 0.0
    outer_rect = Rectangle(pos.x, pos.y, width, height)
    ability_rect = Rectangle(0, 0, width * 0.4, height * 0.2).align_to_rect(outer_rect, "left", "top")
    left_col_rect = Rectangle(0, 0, width * 0.4, height).align_to_rect(outer_rect, "left", "bottom")
    right_col_rect = Rectangle(0, 0, width * 0.6, height).align_to_rect(outer_rect, "right", "bottom")
    ability_score_rect = Rectangle(0, 0, width * 0.4, height * 0.4).align_to_rect(outer_rect, "left", "bottom")
    page.draw_rect(outer_rect, radius=radius)
    page.stroke_width = 0.5
    page.font_size = 10
    page.draw_text_centered(ability_rect, ability)
    page.draw_line(ability_rect.bottom_edge())
    page.draw_line(left_col_rect.right_edge())
    page.draw_line(ability_score_rect.top_edge())
    gap = 1.0
    x = right_col_rect.x1() + gap
    y = right_col_rect.y2() - gap - 2.0
    for p in proficiencies:
        draw_check_box(page, Point(x, y), p)
        y = y - gap - 2.0

def draw_check_box(page, pos, text):
    box = Rectangle(pos.x, pos.y, 2.0, 2.0)
    page.draw_rect(box, radius=1.0, stroke_width=0.25)
    gap = 0.5 
    page.font_size = 6
    text_pos = Point(box.x2() + gap, box.center().y - page.font_height() / 2) 
    page.draw_text(text_pos, text)


def draw_stat_field(page, rect, text):
    page.draw_rect(rect, radius=1.0, stroke_width=1.0) 
    text_rect,_ = rect.top_partition(height=4.0)
    page.font_size = 8
    page.draw_text_centered(text_rect, text)
    page.draw_line(text_rect.bottom_edge(), stroke_width=0.5)

def char_sheet():
    filename = "char_sheet_a6.pdf"
    p = Page(filename, landscape(A6), 5.0)
    p.draw_frame()
    page_frame = p.drawable_rect()

    gap = 1.0

    stats = ["AC", "HP", "SPD", "INI", "PPER", "PRFB"]

    abilities = [
        ["STR", ["Save", "Athlete"]],
        ["DEX", ["Save", "Acrobat", "Sleigh", "Stealth"]],
        ["CON", ["Save"]],
        ["INT", ["Save", "Arcana", "History", "Investig.", "Nature", "Religion"]],
        ["WIS", ["Save", "Animals", "Insight", "Medic", "Perceive", "Survive"]],
        ["CHA", ["Save", "Deceive", "Intimidate", "Perform", "Persuade"]]
    ]

    stat_rect = Rectangle(0, 0, 10.0, 10.0).align_to_rect(page_frame, "left", "top")
    for s in stats:
        draw_stat_field(p, stat_rect, s)
        stat_rect = stat_rect.translate(Point(10.0 + gap, 0.0))

    pos = Point(p.x1(), p.y1())
    for a in abilities:
        draw_ability_field(p, pos, a[0], a[1])
        pos += Point(22.0 + gap, 0)
    p.c.save()


if __name__ == "__main__":
    char_sheet()
