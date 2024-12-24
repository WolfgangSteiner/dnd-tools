from pdf_tools import *
import math

p = Page("pdf/index_cards.pdf", landscape=True)
p.register_font("souvenir/souvenir_demi.ttf", "SouvenirDemi")
p.register_font("souvenir/souvenir_bold_italic.ttf", "SouvenirBoldItalic")

card_rect = Rectangle(0,0,72,95)
content_rect = Rectangle(0,0,card_rect.w * 4, card_rect.h * 2).align_to_rect(p.page_rect())

def do_draw_corners(page, rect, width=15):
    draw_corner(page, rect.get_corner_path("top_left", width=width))
    draw_corner(page, rect.get_corner_path("top_right", width=width))
    draw_corner(page, rect.get_corner_path("bottom_left", width=width))
    draw_corner(page, rect.get_corner_path("bottom_right", width=width))

def draw_corner(page, path):
    for l in path.get_lines():
        page.draw_line_humanized(l, stroke_width=1.0, stroke_color=0)

def draw_card(page, rect, img, draw_corners=True):
    rect = rect.apply_margin(5,5)
    if img:
        bbox = image_bbox(img)
        page.draw_image(img, rect, rotate_to_fit=True)
    if draw_corners:
        do_draw_corners(page, rect)

rects = content_rect.subdivide(2,4)
img_path = "sunless_citadel/"
imgs = ["dragon", "meepo", "yusdrayl", "erky_timbers", "calcryx", ("boss", {'size':2}), "giant_rat", "balsag", "skeleton_archer", "kobold_01", "kobold_02"]

ri = 0

for img in imgs:
    r = rects[ri%8]
    if isinstance(img, tuple):
        img, cfg = img
        if cfg.get('size', 1) == 2:
            ri += 1
            r = r.union(rects[ri%8])

    if not '/' in img:
        img = img_path + img
    draw_card(p, r, "assets/" + img + ".png")
    p.draw_rect(r)
    ri += 1

    if ri%8 == 0:
        p.new_page()

p.save()

