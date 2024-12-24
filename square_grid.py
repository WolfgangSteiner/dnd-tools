from dnd_map.square_grid import draw_square_grid, draw_square_grid_ticks
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from dnd_map import Rect

if __name__ == "__main__":
    c = canvas.Canvas("square_grid.pdf", pagesize=A4)
    #draw_square_grid_ticks(c, Rect.from_canvas(c, margin=5), 15)
    draw_square_grid(c, Rect.from_canvas(c, margin=5), 10)
    c.save()
