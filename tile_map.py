from pdf_tools import Page, Rectangle
from PIL import Image
import pdf_tools.img_tools as img_tools
import tempfile

def draw_crop(page, selection_rect, label, total_map_rect, map_img, scale_factor, draw_label=True):
    page.new_page(landscape=selection_rect.is_landscape())
    crop_rect_img = selection_rect / scale_factor
    w, h = map_img.size
    left_crop = crop_rect_img.x
    right_crop = crop_rect_img.x2
    top_crop = h - crop_rect_img.y2
    bottom_crop = h - crop_rect_img.y1
    assert(left_crop >= 0)
    assert(top_crop >= 0)
    assert(right_crop <= w)
    assert(bottom_crop <= h)
    cropped_img = map_img.crop((left_crop, top_crop, right_crop, bottom_crop))
    page.draw_image(cropped_img, page.page_rect, gray_scale=False)
    if draw_label:
        page.draw_text(page.drawable_rect.top_left(), label)


def tile_selection_rects(total_map_rect, selection_rect, overlap=0.9):
    row_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rects = []
    labels = []
    row_count = 0
    x = selection_rect.x
    y = selection_rect.y
    w = selection_rect.w
    h = selection_rect.h
    while y > total_map_rect.y1 - overlap * h:
        x = total_map_rect.x
        col_count = 0
        while x + w < total_map_rect.x2 + w * overlap:
            rects.append(Rectangle(min(x, total_map_rect.x2 - w), max(y, total_map_rect.y1), w, h))
            labels.append(f"{row_names[row_count]}{col_count + 1}")
            x += w * overlap
            col_count += 1
        y -= h * overlap 
        row_count += 1
    return rects, labels


def compute_selection_rects(total_map_rect, positions, selection_width=297, selection_height=210):
    res = []
    labels = []
    for rx, ry, orientation in positions:
        x = total_map_rect.x + rx * total_map_rect.w
        y = total_map_rect.y + ry * total_map_rect.h
        w = max(selection_width, selection_height) if orientation == "landscape" else min(selection_width, selection_height)
        h = min(selection_width, selection_height) if orientation == "landscape" else max(selection_width, selection_height)
        selection_rect = Rectangle(x, y, w, h)
        selection_rect = selection_rect.move_inside_rect(total_map_rect)
        labels.append(f"[{rx:.2f}, {ry:.2f}]")
        res.append(selection_rect)
    return res, labels


def draw_selection_rects(page, total_map_rect, rects, labels):
    scale_factor = max(total_map_rect.w / page.page_rect.w, total_map_rect.h / page.page_rect.h)
    target_rect_scaled = (total_map_rect / scale_factor)
    target_rect = target_rect_scaled.align_to_rect(page.page_rect)
    offset = target_rect.pos - target_rect_scaled.pos
    for r, l in zip(rects, labels):
        r = r / scale_factor + offset
        page.draw_text_aligned(l, r)
        page.draw_rect(r, stroke_width=2, stroke_color=0.0)


page = Page("pdf/cragmaw.pdf", landscape=True)
filename = "/home/wst/books/dnd/lost_mines_of_phandelver/cragmaw_hideout_2.png"

tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=True)
map_img = Image.open(filename)


map_img = img_tools.crop(map_img, 0.05, 0.05, 0.05, 0.05)
map_img = img_tools.enhance_contrast(map_img, 2.0)
map_img = img_tools.equalize(map_img)
map_img.save(tmp.name)

img_w_px, img_h_px = map_img.size
img_w_mm = 297 * 4
scale_factor = img_w_mm / img_w_px

total_map_rect = Rectangle(w=img_w_px, h=img_h_px) * scale_factor
selection_rect = Rectangle(w=297, h=210).align_to_rect(total_map_rect,"left","top")
#rects, labels = tile_selection_rects(total_map_rect, selection_rect)
L = "landscape"
P = "portrait"

px_offset = 0.2 - 0.04
rects, labels = compute_selection_rects(total_map_rect, (
    (0.04, 0.02, P), (0.04 + px_offset, 0.02, P), (0.04 + 2*px_offset, 0.02, P), (0.04 + 3*px_offset, 0.02, P),
    (0.04 + 2*px_offset, 0.36, P),
    (0.13 + 2*px_offset, 0.28, P),
    (3.85*px_offset, 0.13, P), (4.85*px_offset, 0.12, P), # Klarg's lair
    (2.9*px_offset, 0.55, P), (3.9*px_offset, 0.44, P), (4.9*px_offset, 0.44, P), (3.85*px_offset, 0.65, L), # twin pool room
    (1.4*px_offset, 0.7, L), # upper corridor 
    (1.4*px_offset, 0.55, L), # lower corridor
    (0.0, 0.46, P), (0.0 + px_offset, 0.44, P), 
))


page.draw_image(map_img, page.page_rect)

draw_selection_rects(page, total_map_rect, rects, labels)

for r, l in zip(rects, labels):
    assert total_map_rect.contains_rect(r)
    draw_crop(page, r, l, total_map_rect, map_img, scale_factor, draw_label=False)

page.save()
