from dnd_map.square_grid import draw_square_grid, draw_square_grid_ticks
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdf_tools import Page, Rectangle, Point, Line

if __name__ == "__main__":
    p = Page("pdf/square_grid.pdf", pagesize=A4)
    #draw_square_grid_ticks(c, Rect.from_canvas(c, margin=5), 15)
    draw_square_grid(p, 25)
    p.save()
