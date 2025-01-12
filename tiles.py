from pdf_tools import Page, Rectangle, Line


page = Page("pdf/tiles.pdf")


def draw_tile(page, rect, filename):
    page.draw_image(filename, rect)



pos = page.drawable_rect.top_left()

rect = Rectangle(pos.x, pos.y, 40, 40).align_to_rect(page.drawable_rect, "left", "top")

draw_tile(page, rect, "assets/bocca.png")

page.save()
