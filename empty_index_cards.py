from pdf_tools import *
from pdf_tools.ornaments import draw_rect_corners_humanized
import math
from types import SimpleNamespace 

page = Page("pdf/empty_index_cards.pdf", landscape=True)
page.register_font("souvenir/souvenir_demi.ttf", "SouvenirDemi")
page.register_font("souvenir/souvenir_bold_italic.ttf", "SouvenirBoldItalic")

cfg = SimpleNamespace(stroke_color=0.0, stroke_width=1.0)

for rows, cols in ((2,2),(2,4),(4,4),):
    for r in page.subdivide(rows, cols):
        r = r.apply_margin(5,5)
        draw_rect_corners_humanized(page, r, cfg)

    page.new_page()

page.save()

