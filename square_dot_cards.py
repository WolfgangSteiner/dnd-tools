from dnd_map.square_grid import draw_square_dot_cards
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

if __name__ == "__main__":
    c = canvas.Canvas("square_dot_cards.pdf", pagesize=A4)
    for s in ((1,1), (2,1), (2,2), (3, 2), (4, 2), (4, 4)):
        draw_square_dot_cards(c, s, grid_size=15, radius=0.2)
        c.showPage()
    c.save()
