from dnd_map.square_grid import draw_square_grid, draw_square_grid_ticks, draw_square_grid_cards
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A5,A6,A7

if __name__ == "__main__":
    c = canvas.Canvas("square_grid_cards.pdf", pagesize=A4)
    for s in ((1,1), (2,1), (2,2), (3, 2), (4, 2), (4, 4)):
        draw_square_grid_cards(c, s)
        c.showPage()
    c.save()
