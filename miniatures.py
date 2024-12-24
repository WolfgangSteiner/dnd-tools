from pdf_tools import Page, Rectangle, Line, Point, image_bbox
import argparse

DEFAULT_WIDTH = 25

def place_bbox(page, union_rect, bbox):
    if bbox.w + union_rect.w > page.drawable_rect().w:
        pos = union_rect.bottom_left()
        union_rect = Rectangle(pos.x, pos.y, 0, 0)

    pos = union_rect.top_right()
    bbox = bbox.translate(pos - Point(0, bbox.h))
    union_rect = union_rect.union(bbox)

    return union_rect, bbox

def draw_miniature(page, union_rect, name, stand_height=6, stand_width=20, width_factor=1.0):
    page.stroke_color=0.75
    page.stroke_width=0.5
    if name.startswith("ph:"):
        name = name.split("ph:")[1]
        return draw_miniature_printableheroes(page, union_rect, name, width_factor=width_factor)

    filename = f"assets/{name}.png"
    img_bbox = image_bbox(filename, width=DEFAULT_WIDTH*width_factor)
    bbox = img_bbox.copy()
    bbox.h = bbox.h * 2 + 2 * stand_height
    union_rect, bbox = place_bbox(page, union_rect, bbox)
    upper, lower = bbox.top_partition(0.5)
    page.draw_line(upper.bottom_edge())
    upper = img_bbox.align_to_rect(upper, vertical_align="bottom")
    page.draw_image(filename, upper, flip_vertically=True)
    lower = img_bbox.align_to_rect(lower, vertical_align="top")
    page.draw_image(filename, lower)
    stand_box = Rectangle(0, 0, stand_width, stand_height)
    stand_box = stand_box.align_to_rect(bbox, vertical_align="top")
    page.draw_rect(stand_box)
    stand_box = stand_box.align_to_rect(bbox, vertical_align="bottom")
    page.draw_rect(stand_box)
    page.draw_rect(bbox) 
    return union_rect 


def draw_miniature_printableheroes(page, union_rect, name, width_factor=1.0):
    filename = f"assets/printableheroes/{name}.png"
    bbox = image_bbox(filename, width=DEFAULT_WIDTH*width_factor)
    union_rect, bbox = place_bbox(page, union_rect, bbox)
    page.draw_image(filename, bbox)

    return union_rect
     

page = Page("pdf/miniatures.pdf")
pos = page.drawable_rect().top_left()


miniatures = [("inferno_spider", 2, 1.5), ("ph:giant_centipede", 5, 1.0)]
miniatures = [("ph:wizard_0202", 1, 0.75 * 20/13),("ph:half_elf_cleric_03", 1, 20/13), ("ph:dwarf_warrior", 1, 20/12), ("ph:elf_ranger_01", 1, 20/16)]
union_rect = Rectangle(pos.x, pos.y, 0, 0)
for m in miniatures:
    for i in range(m[1]):
        union_rect = draw_miniature(page, union_rect, m[0], width_factor=m[2])


page.save()
