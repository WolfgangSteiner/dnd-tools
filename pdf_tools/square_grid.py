from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from math import floor
from reportlab.lib.pagesizes import A4, A5, A6, A7
from pdf_tools import Rectangle, Point

def print_rect(tag, rect):
    print(f"{tag}: {rect.x}, {rect.y}, {rect.w}, {rect.h}")


def draw_square_grid(page, grid_size, margin=5, line_width=0.25, lightness=0.75):
    rect = page.page_rect().apply_margin(margin, margin)
    squares_per_row = floor(rect.w / grid_size)
    squares_per_col = floor(rect.h / grid_size)

    grid_width = squares_per_row * grid_size
    grid_height = squares_per_col * grid_size
    grid_rect = Rectangle(0, 0, grid_width, grid_height).align_to_rect(rect)

    page.stroke_width = line_width
    page.stroke_color = lightness

    for r in grid_rect.subdivide(squares_per_col, squares_per_row):
        page.draw_rect(r)

    #y = grid_rect.y
    #while y <= grid_rect.y2():
    #    page.line(grid_rect.x * mm, y * mm, grid_rect.x2() * mm, y * mm)
    #    y += grid_size

    #x = grid_rect.x
    #while x <= grid_rect.x2():
    #    canvas.line(x * mm, grid_rect.y * mm, x * mm, grid_rect.y2() * mm)
    #    x += grid_size


def draw_square_grid_ticks(canvas, rect, grid_size, tick_length=1, line_width=0.25, lightness=0.75):
    squares_per_row = floor(rect.w / grid_size)
    squares_per_col = floor(rect.h / grid_size)

    grid_width = squares_per_row * grid_size
    grid_height = squares_per_col * grid_size
    grid_rect = Rect(0, 0, grid_width, grid_height).align_to_rect(rect)

    canvas.setLineWidth(line_width)
    canvas.setStrokeGray(lightness)

    y = grid_rect.y
    while y <= grid_rect.y2():
        x = grid_rect.x - grid_size
        while x <= grid_rect.x2():
            canvas.line(x * mm, y * mm, (x + tick_length) * mm, y * mm)
            x += grid_size
            canvas.line(x * mm, y * mm, (x - tick_length) * mm, y * mm)
        y += grid_size

    x = grid_rect.x
    while x <= grid_rect.x2():
        y = grid_rect.y - grid_size 
        while y <= grid_rect.y2():
            canvas.line(x * mm, y * mm, x * mm, (y + tick_length) * mm)
            y += grid_size
            canvas.line(x * mm, y * mm, x * mm, (y - tick_length) * mm)
        x += grid_size


def draw_square_grid_cards(canvas, rows_cols, margin=5, grid_size=10, draw_frame=True):
    canvas_rect = Rect.from_canvas(canvas, margin=5)
    rows, cols = rows_cols

    for r in canvas_rect.subdivide(rows, cols):
        draw_square_grid(canvas, r.apply_margin(margin, margin), grid_size=grid_size)
        if draw_frame:
            r.draw(canvas)


def draw_square_grid_dots(page, rect, grid_size, tick_length=1, stroke_width=0.25, lightness=0.7, alternate=False, center_points=False):
    squares_per_row = floor(rect.w / grid_size)
    squares_per_col = floor(rect.h / grid_size)

    grid_width = squares_per_row * grid_size
    grid_height = squares_per_col * grid_size
    grid_rect = Rectangle(0, 0, grid_width, grid_height).align_to_rect(rect)

    page.stroke_width = stroke_width
    page.stroke_color = lightness

    p = grid_rect.top_left()

    for row in range(squares_per_col + 1):
        p.x = grid_rect.x 
        for col in range(squares_per_row + 1):
            if alternate == False or (row % 2) != (col % 2):
                page.draw_dot(p, lightness)
            p.x += grid_size
        p.y -= grid_size

    if center_points:
        p = grid_rect.top_left() - Point(grid_size / 2, grid_size / 2)
        for row in range(squares_per_col):
            p.x = grid_rect.x + grid_size / 2
            for col in range(squares_per_row):
                if alternate == False or (row % 2) != (col % 2):
                    page.draw_dot(p,lightness)
                p.x += grid_size
            p.y -= grid_size

def draw_square_dot_cards(page, rows_cols, margin=5, grid_size=10, draw_frame=True, alternate=False, center_points=False):
    rect = page.page_rect()
    rows, cols = rows_cols

    for r in rect.subdivide(rows, cols):
        draw_square_grid_dots(page, r.apply_margin(margin, margin), grid_size=grid_size, alternate=alternate, center_points=center_points)
        if draw_frame:
            page.draw_rect(r)




