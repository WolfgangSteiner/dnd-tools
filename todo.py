from pdf_tools import Page
from pdf_tools.ornaments import draw_rect_corners_humanized

page = Page("pdf/todo_cards.py", landscape=True)

rects = page.subdivide(4,4)

[page.draw_rect(r) for r in rects ]


page.save()
