import sys
import math
import random
from math import sin, cos, pi, tan
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import numpy as np
import copy

from dnd_map import draw_forest



def draw_hex_grid(canvas, hex_width):
    """Draw a hexagonal grid on an A4 sheet."""
    # A4 page dimensions in points (1 pt = 1/72 inch)
    page_width, page_height = A4

    # Hexagon geometry
    hex_radius = (hex_width / 2) / cos(pi / 6)
    hex_height = 2 * hex_radius
    vertical_step = hex_width / 2 * tan(pi / 6) + hex_radius
    horizontal_step = hex_width

    # Create a canvas
    c.setLineWidth(0.25)
    c.setStrokeGray(0.75)

    # Draw hexagons row by row
    y = 0
    row = 0
    while y - hex_height / 2 < page_height:
        # Determine x offset for even/odd rows
        x_offset = 0 if row % 2 == 0 else hex_width / 2

        x = x_offset
        while x - hex_width / 2 < page_width:
            draw_hexagon(c, x, y, hex_radius, rotated=True)
            x += horizontal_step

        y += vertical_step
        row += 1


def draw_hexagon(c, x, y, size, rotated):
    """Draw a single hexagon centered at (x, y) with the given size."""
    angle = math.pi / 3  # 60 degrees
    path = c.beginPath()  # Create a new path object for the hexagon
    rot = math.pi / 6 if rotated else 0.0

    for i in range(6):
        px = x + size * math.cos(i * angle + rot)
        py = y + size * math.sin(i * angle + rot)
        if i == 0:
            path.moveTo(px, py)  # Start the path at the first vertex
        else:
            path.lineTo(px, py)  # Draw a line to the next vertex

    path.close()  # Close the hexagon path
    c.drawPath(path, stroke=1, fill=0)  # Draw the path on the canvas


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hex_grid.py <hex_radius> <output_file>")
        sys.exit(1)

    try:
        hex_radius = float(sys.argv[1])
        if hex_radius <= 0:
            raise ValueError
    except ValueError:
        print("Error: <hex_radius> must be a positive number.")
        sys.exit(1)

    output_file = sys.argv[2]
    c = canvas.Canvas(output_file, pagesize=A4)
    page_width, page_height = A4
    draw_forest(c, page_width, page_height)
    draw_hex_grid(c, hex_radius * mm)

    c.save()

