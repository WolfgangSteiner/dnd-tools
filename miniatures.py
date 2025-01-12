from pdf_tools import Page, Rectangle, Line, Point, image_bbox
import argparse
import os
import glob
import typer
from PIL import Image
from typing import List

DEFAULT_WIDTH = 25
DEFAULT_BASE_WIDTH = 20

def place_bbox(page, union_rect, bbox):
    if bbox.w + union_rect.x2 > page.drawable_rect.x2:
        pos = union_rect.bottom_left()
        union_rect = Rectangle(pos.x, pos.y, 0, 0)

    if union_rect.y2 - bbox.h < page.drawable_rect.y1:
        page.new_page()
        union_rect = Rectangle(page.drawable_rect.x1, page.drawable_rect.y2, 0, 0)

    pos = union_rect.top_right()
    bbox = bbox.translate(pos - Point(0, bbox.h))
    union_rect = union_rect.union(bbox)

    return union_rect, bbox

def draw_miniature(
    page,
    union_rect,
    name,
    width_factor=1.0,
    extra_margin:bool=True,
    draw_name:bool=True,
    stand_height=6,
    stand_width=20,
):
    page.stroke_color=0.75
    page.stroke_width=0.5

    if name.startswith("ph:"):
        filename = name.replace("ph:", "assets/printableheroes/")
    elif name.startswith("assets/"):
        filename = name
    else:
        filenames = glob.glob(f"assets/**/{name}.png", recursive=True)
        if len(filenames) != 1:
            print(f"Cound not find image file for name {name}")
            raise ValueError
        filename = filenames[0]
    
    if filename.startswith("assets/printableheroes/"):
        return draw_miniature_printableheroes(
            page,
            union_rect,
            filename,
            width_factor=width_factor,
            extra_margin=extra_margin,
            draw_name=draw_name
        )

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
    stand_height = 2*stand_height if draw_extra_margin else stand_height
    stand_box = Rectangle(0, 0, stand_width, stand_height)
    stand_box = stand_box.align_to_rect(bbox, vertical_align="top")
    page.draw_rect(stand_box)
    stand_box = stand_box.align_to_rect(bbox, vertical_align="bottom")
    page.draw_rect(stand_box)
    page.draw_rect(bbox) 
    return union_rect 


def is_horizontal_line(img, y):
    w,h = img.size
    color = img.getpixel((w//2,y))
    count = 0
    color = (0,0,0,255)
    for x in range(w):
        if is_border_pixel(img.getpixel((x,y))):
            count+=1
    return count / w > 0.95

def get_horizontal_lines(img):
    result = []
    w, h = img.size
    for y in range(h//32,h//8):
        if is_horizontal_line(img, y):
            result.append(y)
    return result

def is_border_pixel(val):
    thres = 32
    return val != (0,0,0,0)
    return val == (0,0,0,255)
    return val[0] < thres and val[1] < thres and val[2] < thres and val[3] == 255 

def is_border_pixel_at(img, x, y):
    return is_border_pixel(img.getpixel((x,y)))


def has_border_pixels(img, y):
    for x in range(img.size[0]):
        if is_border_pixel(img.getpixel((x,y))):
            return True
    return False

def has_nonzero_pixels(img, y):
    for x in range(img.size[0]):
        if (0,0,0,0) != img.getpixel((x,y)):
            return True
    return False


def print_debug_img(img):
    w,h = img.size
    for y in range(0, h//8):
        line = ""
        for x in range(0, w, 2):
            val1 = img.getpixel((x,y)) != (0,0,0,0)
            val2 = img.getpixel((x+1,y)) != (0,0,0,0)
            c = "x" if val1 or val2 else " "
            line += c
        print(f"{y:03d} {line}")

def find_base_boundary_left(img, y):
    x = 0
    while is_border_pixel_at(img, x, y):
        x += 1

    while not is_border_pixel_at(img, x, y):
        x += 1
    return x

def find_base_boundary_right(img, y):
    x = img.size[0] - 1
    while is_border_pixel_at(img, x, y):
        x -= 1

    while not is_border_pixel_at(img, x, y):
        x -= 1
    return x

def determine_base_width(filename):
    with Image.open(filename) as img:
        w, h = img.size
        horizontal_lines = get_horizontal_lines(img)
        base_line_y = horizontal_lines[0]
        print(f"{filename}: {horizontal_lines} base_line at: {base_line_y}")
        y = base_line_y - 1
        x1 = find_base_boundary_left(img, y)
        x2 = find_base_boundary_right(img, y)

        base_line_width = x2 - x1
        if base_line_width <= 0:
            base_line_width = w // 2

        return base_line_width, w
    return 0

def file_stem(filename):
    return os.path.splitext(os.path.split(filename)[1])[0]


def draw_miniature_printableheroes(
    page,
    union_rect,
    name,
    width_factor=1.0,
    extra_margin:bool=True,
    draw_name:bool=True
):
    if not name.startswith("assets/printableheroes"):
        name = "assets/printableheroes/" + name
    if not name.endswith(".png"):
        name = name + ".png"
    base_width_px, img_width_px = determine_base_width(name)
    base_width = DEFAULT_BASE_WIDTH * width_factor
    pixels_per_mm = base_width_px / base_width 
    total_width = img_width_px / pixels_per_mm
    bbox = image_bbox(name, width=total_width)
    if extra_margin:
        bbox.h += 14

    def do_draw(page, rect, name):
    #union_rect, bbox = place_bbox(page, union_rect, bbox)
        page.draw_rect(rect)
        page.draw_image(name, rect)
        if draw_name:
            page.draw_text_aligned(file_stem(name), bbox.apply_margin(y=3), vertical_align="bottom")

    page.push_layout_rect(bbox, lambda the_page, the_rect: do_draw(the_page, the_rect, name))

    return union_rect
     


def draw_miniatures(
    page,
    miniatures,
    extra_margin:bool=True,
    draw_name:bool=True
):
    pos = page.drawable_rect.top_left()
    union_rect = Rectangle(pos.x, pos.y, 0, 0)

    filenames = []

    for m in miniatures:
        name, count, width_factor = m
        name, count, width_factor = m

        if name.startswith("ph:"):
            filename = name.replace("ph:", "assets/printableheroes/")
            filenames.append((filename, count, width_factor))
        elif name.startswith("assets/"):
            filename = name
            filenames.append((filename, count, width_factor))
        else:
            glob_names = glob.glob(f"assets/**/{name}.png", recursive=True)
            for filename in glob_names:
                filenames.append((filename, count, width_factor))
                
    for m in filenames:
        name, count, width_factor = m
        for i in range(count):
            union_rect = draw_miniature(
                page,
                union_rect,
                name,
                width_factor=width_factor,
                extra_margin=extra_margin,
                draw_name=draw_name
            )
    page.perform_layout()
    page.new_page()

def list_get(list, idx, default=None):
    return list[idx] if idx < len(list) else default


def main(
    files: List[str],
    repeat: int = 1,
    extra_margin:bool = True,
    draw_name: bool = True,
):
    miniatures = []
    for file_name in files:
        args = tuple() 
        if ":" in file_name:
            file_name, args = file_name.split(":", 1)
            args = args.split(":")
        for file_name in glob.glob(file_name):
            miniatures.append(
                (file_name,
                int(list_get(args, 0, repeat)),
                float(list_get(args, 1, 1.0))
                )
            )


    if len(miniatures) == 0:
        print("No miniatures found.")

    page = Page("pdf/miniatures.pdf")
    draw_miniatures(page, miniatures, extra_margin=extra_margin, draw_name=draw_name)
    page.save()

if __name__ == "__main__":
    typer.run(main)

