from .dnd_map import Object, Path, Point
from math import sin, cos, tan, pi
import random
import numpy as np
from reportlab.lib.units import mm

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
    c.setFillColorRGB(0.2,0.5,0.3)
    c.setLineJoin(1) # round line joins 
    c.setLineWidth(0.5)           # Thin outline
    o.draw(c)


def draw_forest(canvas, width, height, num_trees=20, tree_radius_range=(40, 60)):
    """
    Draw a forest of randomly placed trees.

    :param output_file: Output PDF file
    :param num_trees: Number of trees to draw
    :param tree_radius_range: (min, max) radius for the trees
    """
    c = canvas

    rng = random.Random()
    rng.seed(42)

    size = 40
    seed = 0

    for y in np.arange(size / 2 * mm, height, size * mm):
        for x in np.arange(size / 2 * mm, width, size * mm):
            draw_tree(c, Point(x, y), 50, seed=seed)
            seed += 1


