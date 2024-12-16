import sys
import math
import random
from math import sin, cos, pi, tan
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import numpy as np
import copy

class Object:
    def __init__(self):
        self.paths = []
        self.new_path()
        self.connect_paths = False
        self.close_connected_paths = False

    def new_path(self):
        self.add_path(Path())

    def add_path(self, path):
        self.current_path = path
        self.paths.append(path)

    def close_path(self):
        self.current_path.close()
        self.new_path()

    def add_point(self, x, y):
        self.current_path.add_point(x,y)

    def merge_object(self, obj):
        for p in obj.paths:
            self.add_path(copy.deepcopy(p))

    def merge_paths(self):
        new_path = Path() 
        new_paths = [new_path]
        for path in self.paths:
            for p in path.points:
                new_path.points.append(p)
        self.paths = new_paths
        self.current_path = new_path

    def draw(self, canvas):
        for p in self.paths:
            p.draw(canvas)


class Path:
    def __init__(self):
        self.points = []
        self.closed = False

    def add_point(self, x, y):
        self.points.append(Point(x,y))

    def close(self):
        self.closed = True

    def draw(self, canvas):
        if len(self.points) == 0:
            return
        path = canvas.beginPath()
        path.moveTo(self.points[0].x, self.points[0].y)
        for i in range(1, len(self.points)):
            path.lineTo(self.points[i].x, self.points[i].y)
        if self.closed:
            path.close()
        canvas.drawPath(path, stroke=1, fill=0)

    def merge_path(self, path):
        for p in path.points:
            self.points.append(p)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



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


def generate_noisy_circle(center, radius, rng=random.Random(), irregularity=0.1, points=40, broken=False):
    o = Object()
    angle_step = 2 * pi / points
    for i in range(points):
        angle = i * angle_step
        # Add random irregularity to the radius
        r = radius * (1 + rng.uniform(-irregularity, irregularity))
        x = center.x + r * cos(angle)
        y = center.y + r * sin(angle)
        o.add_point(x, y)
    o.close_path()
    return o


def generate_tree_points(center, radius, seed=None, irregularity=0.1, points=40, layers=5, layer_scale=0.75, min_layer_scale=0.25):
    o = Object()
    rng = random.Random()
    rng.seed(seed)
    scale = layer_scale
    num_leaves = 12
    density = 0.75
    outer_circle = generate_leaf_circle(center, radius, max_num_leaves=num_leaves, density=1.0, rng=rng)
    outer_circle.merge_paths()
    outer_circle.current_path.close()
    o.merge_object(outer_circle)
    while scale >= min_layer_scale:
        if True:
            leaves = generate_leaf_circle(center, radius*scale, max_num_leaves=num_leaves, rng=rng, density=density)
        else:
            leaves = generate_noisy_circle(center, radius*scale, rng=rng)
        o.merge_object(leaves)
        num_leaves *= 0.9
        scale *= layer_scale
        density *= 0.8

    o.merge_object(generate_noisy_circle(center, radius*0.1, rng=rng, irregularity=0.2, points=20))
    return o


def generate_tree_leaf(center, radius, angle, leaf_radius=2, leaf_angle=2*pi*0.6, rng=random.Random(), irregularity=0.125):
    o = Object()
    cx = center.x + (radius - leaf_radius) * cos(angle)
    cy = center.y + (radius - leaf_radius) * sin(angle)
    num_points = 20
    phi = angle - leaf_angle / 2
    for i in range(num_points):
        r = leaf_radius * (1 + rng.uniform(-1.0, 1.0) * irregularity)
        x = cx + r * cos(phi)
        y = cy + r * sin(phi)
        phi += leaf_angle / num_points
        o.add_point(x,y)
    return o


def generate_leaf_circle(center, radius, density=0.4, max_num_leaves=12, rng=None, irregularity=0.1, radius_irregularity=0.1):
    o = Object()
    num_leaves = int(rng.uniform(0.75, 1.0) * max_num_leaves + 0.5)
    leaf_angle = 2*pi / num_leaves
    phi = rng.uniform(0.0, 2*pi/num_leaves)
    for i in range(num_leaves):
        show_leaf = rng.random() < density
        delta_phi = 0 * rng.uniform(-0.25, 0.25) * leaf_angle
        delta_radius = 1.0 + radius_irregularity * rng.uniform(-1.0, 1.0)
        if show_leaf:
            o.merge_object(generate_tree_leaf(center, delta_radius * radius, phi + delta_phi, radius*0.2))
        phi += leaf_angle
    return o


def draw_tree(c, center, radius, seed=42):
    """
    Draw a single tree on the canvas.

    :param c: ReportLab canvas
    :param center: X-coordinate of the tree center
    :param radius: Average radius of the tree shape
    """
    # Generate tree shape points
    o = generate_tree_points(center, radius, seed=seed)

    # Start the path
    c.setStrokeColorRGB(0, 0, 0)  # Black outline
    c.setLineJoin(1) # round line joins 
    c.setLineWidth(0.5)           # Thin outline
    o.draw(c)


def draw_forest(canvas, num_trees=20, tree_radius_range=(40, 60)):
    """
    Draw a forest of randomly placed trees.

    :param output_file: Output PDF file
    :param num_trees: Number of trees to draw
    :param tree_radius_range: (min, max) radius for the trees
    """
    page_width, page_height = A4
    c = canvas

    rng = random.Random()
    rng.seed(42)

    size = 40
    seed = 0

    for y in np.arange(size / 2 * mm, page_height, size * mm):
        for x in np.arange(size / 2 * mm, page_width, size * mm):
            draw_tree(c, Point(x, y), 50, seed=seed)
            seed += 1


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
    draw_forest(c)
    draw_hex_grid(c, hex_radius * mm)

    c.save()

