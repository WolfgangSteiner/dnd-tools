from pdf_tools.square_grid import draw_square_dot_cards
from pdf_tools import Page

if __name__ == "__main__":
    page = Page("pdf/square_dot_grid.pdf")
    for s in ((1,1), (2,1), (2,2), (3, 2), (4, 2), (4, 4)):
        draw_square_dot_cards(page, s, grid_size=5, margin=5, alternate=False, center_points=True)
        page.new_page()
    page.save()
