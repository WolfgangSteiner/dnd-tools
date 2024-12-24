from .rectangle import Rectangle
from PIL import Image

def crop_transparent_pixels(img):
    if img.mode == "RGBA":
        alpha = img.split()[3]  # Get the alpha channel
        bbox = alpha.getbbox()
        return img.crop(bbox)
    else:
        return img


def image_bbox(filename, width=None, height=None, ppi=300):
    ppmm = ppi / 2.54 * 10
    with Image.open(filename) as img:
        img = crop_transparent_pixels(img)
        w, h = img.size

    aspect_ratio = w / h

    if width is not None:
        w = width
        h = width / aspect_ratio
    elif height is not None:
        h = height
        w = height * aspect_ratio
    else:
        w /= ppmm
        h /= ppmm

    return Rectangle(0, 0, w ,h)

