from .rectangle import Rectangle
from PIL import Image, ImageEnhance, ImageOps

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
        w /= ppmm, Int
        h /= ppmm

    return Rectangle(0, 0, w ,h)


def crop(img, left=0, right=0, top=0, bottom=0): 
    img_w, img_h = img.size
    left_crop = left * img_w
    right_crop = img_w - right * img_w
    top_crop = top * img_h
    bottom_crop = img_h - bottom * img_h
    crop_box = (left_crop, top_crop, right_crop, bottom_crop)
    return img.crop(crop_box)


def flip_vertically(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def rotate(img):
    return img.transpose(Image.ROTATE_90)


def enhance_contrast(img, factor=2):
    enh = ImageEnhance.Contrast(img.convert('L'))
    return enh.enhance(factor)

def equalize(img):
    return ImageOps.equalize(img)

    
