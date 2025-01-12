from .point import Point
from .line import Line
from .rectangle import Rectangle
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
import reportlab.lib.pagesizes as pagesizes
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PIL import Image, ImageEnhance, ImageOps
import tempfile
from .img_tools import crop_transparent_pixels
from . import img_tools
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from types import SimpleNamespace
import copy
import re

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet

def get_arg(arg, default):
    return default if arg is None else arg

KERNING = {"SouvenirDemi":{
    "At":-0.15, "Ja":-0.1, "Pa":-0.3, "Pe":-0.1, "Pr":-0.1, "Ro":-0.1, "Th":-0.25, "To":-0.25, "Tr":-0.2, "Wa":-0.3, "We":-0.15}}
KERNING["SouvenirBold"] = KERNING["SouvenirDemi"]

class Page:
    A3 = pagesizes.A3
    A4 = pagesizes.A4
    A5 = pagesizes.A5
    A6 = pagesizes.A6

    def __init__(self, filename=None, pagesize=pagesizes.A4, margin=5, landscape=False):
        filename = get_arg(filename, "pdf/out.pdf")
        pagesize = pagesizes.landscape(pagesize) if landscape == True else pagesize
        self.c = canvas.Canvas(filename)
        self.font_path = "~/.local/share/fonts" 
        self.state_stack = [SimpleNamespace()]
        self.set_pagesize(pagesize)

        self.left_margin = margin
        self.right_margin = margin
        self.top_margin = margin
        self.bottom_margin = margin
        self.stroke_width = 0.25
        self.stroke_color = 0.5
        self.fill_color = 0
        self.font_size = 10
        self.small_caps_factor = 0.65

        self.register_font("souvenir/souvenir.ttf", "Souvenir")
        self.register_font("souvenir/souvenir_demi.ttf", "SouvenirDemi")
        self.register_font("souvenir/souvenir_bold.ttf", "SouvenirBold")
        self.register_font("souvenir/souvenir_italic.ttf", "SouvenirItalic")
        self.register_font("souvenir/souvenir_bold_italic.ttf", "SouvenirBoldItalic")
        self.register_font("roboto_slab/roboto_slab_bold.ttf", "RobotoSlabBold")
        self.register_font("roboto_slab/roboto_slab_semibold.ttf", "RobotoSlab-SemiBold")
        self.register_font("roboto_slab/roboto_slab_regular.ttf", "RobotoSlab")
        self.register_font("tangerine/tangerine_regular.ttf", "Tangerine")
        self.register_font("tangerine/tangerine_bold.ttf", "TangerineBold")
        self.register_font_family("Souvenir", "Souvenir", bold="SouvenirBold", italic="SouvenirItalic")
        self.register_font_family("RobotoSlab", "RobotoSlab", bold="RobotoSlabBold")
        self.layout_rect_list = []

    @property
    def state(self):
        return self.state_stack[-1]

    @property
    def font(self):
        return getattr(self.state, "font", "Helvetica")
    @font.setter
    def font(self, value):
        self.state.font = value

    @property
    def stroke_width(self):
        return getattr(self.state, "stroke_width", "Helvetica")
    @stroke_width.setter
    def stroke_width(self, value):
        self.state.stroke_width = value

    @property
    def stroke_color(self):
        return getattr(self.state, "stroke_color", "Helvetica")
    @stroke_color.setter
    def stroke_color(self, value):
        self.state.stroke_color = value


    def set_pagesize(self, pagesize, landscape=False):
        if landscape:
            h, w = pagesize
        else:
            w, h = pagesize
        self.pagesize = (w,h)
        self.w = w / mm
        self.h = h / mm
        self.c.setPageSize(self.pagesize)

    def set_landscape(self):
        new_w = max(self.w, self.h)
        new_h = min(self.w, self.h)
        self.w = new_w
        self.h = new_h
        self.pagesize = (new_w * mm, new_h * mm)
        self.c.setPageSize(self.pagesize)

    def set_portrait(self):
        new_w = min(self.w, self.h)
        new_h = max(self.w, self.h)
        self.w = new_w
        self.h = new_h
        self.pagesize = (new_w * mm, new_h * mm)
        self.c.setPageSize(self.pagesize)
        

    def set_page_rect(self, rect):
        self.set_pagesize((rect.w * mm, rect.h * mm))


    @property
    def drawable_rect(self):
        return Rectangle(self.left_margin, self.bottom_margin, self.w - self.left_margin - self.right_margin, self.h - self.bottom_margin - self.top_margin)

    @property
    def page_rect(self):
        return Rectangle(0, 0, self.w, self.h)

    def draw_frame(self):
        self.draw_rect(self.drawable_rect())

    def x1(self):
        return self.left_margin

    def x2(self):
        return self.w - self.right_margin

    def y1(self):
        return self.bottom_margin

    def y2(self):
        return self.h - self.top_margin


    def draw_rect(self, r, stroke_width=None, stroke_color=None, radius=None):
        self.push_state()
        stroke_color = get_arg(stroke_color, self.stroke_color)
        stroke_width = get_arg(stroke_width, self.stroke_width)
        self.c.setStrokeGray(stroke_color)
        self.c.setLineWidth(stroke_width)
        if radius is not None:
            radius = radius
        elif r.radius is not None:
            radius = r.radius
        else:
            radius = 0

        if radius:
            self.c.roundRect(r.x * mm, r.y * mm, r.w * mm, r.h * mm, radius * mm, stroke = 1, fill = 0)
        else:
            self.c.rect(r.x * mm, r.y * mm, r.w * mm, r.h * mm, stroke=1, fill=0)
        self.pop_state()

    def fill_rect(self, rect, radius=0.0, fill_color=None):
        self.c.saveState()
        self.c.setFillGray(self.fill_color if fill_color == None else fill_color)
        if radius == 0.0:
            self.c.rect(rect.x*mm, rect.y*mm, rect.w*mm, rect.h*mm, stroke=0, fill=1)
        else:
            self.c.roundRect(rect.x*mm, rect.y*mm, rect.w*mm, rect.h*mm, radius=radius *mm, stroke=0, fill=1)
        self.c.restoreState()


    def _is_small_caps_upper(char):
        return char.isupper() or re.match(r'[0-9+-/&()]', char)

    def _get_small_caps_upper_prefix(word):
        res = ""
        while len(word) and Page._is_small_caps_upper(word[0]):
            res += word[0]
            word = word[1:]
        return res, word

    def _get_small_caps_lower_prefix(word):
        res = ""
        while len(word) and not Page._is_small_caps_upper(word[0]):
            res += word[0]
            word = word[1:]
        return res, word

    def draw_text(self, pos, text, font=None, font_size=None, small_caps=False, color=0.0):
        font = self.font if font is None else font
        font_size = self.font_size if font_size is None else font_size
        text = str(text)
        self.push_state()
        self.c.setFillGray(color)
        if small_caps:
            small_font_size = self.small_caps_factor * font_size
            en_space = small_font_size / 2 / mm
            x = pos.x
            is_first = True


            while text.startswith(" "):
                x += en_space
                text = text[1:]

            for word in text.split():
                if is_first:
                    is_first = False
                else:
                    x += en_space

                while len(word):
                    upper_prefix, word = Page._get_small_caps_upper_prefix(word)
                    if upper_prefix:
                        bbox = self.text_bounding_box(upper_prefix, font=font, font_size=font_size)
                        kerning_adjustment = self.get_kerning_adjustment(upper_prefix, word, font, font_size)
                        self.c.setFont(font, font_size)
                        self.c.drawString(x * mm, pos.y * mm, upper_prefix)
                        x += bbox.w + kerning_adjustment
                    
                    lower_prefix, word = Page._get_small_caps_lower_prefix(word)
                    if lower_prefix:
                        bbox = self.text_bounding_box(lower_prefix.upper(), font=font, font_size=small_font_size)
                        self.c.setFont(font, small_font_size)
                        self.c.drawString(x * mm, pos.y * mm, lower_prefix.upper())
                        x += bbox.w
                    
        else:
            self.c.setFont(font, font_size)
            self.c.drawString(pos.x * mm, pos.y * mm, text)

        self.pop_state()

    def font_height(self, font=None, font_size=None):
        font = get_arg(font, self.font)
        font_size = get_arg(font_size, self.font_size)
        face = pdfmetrics.getFont(font).face
        return (face.ascent) / 1000 * font_size / mm

    def text_width(self, text, font=None, font_size=None):
        font = get_arg(font, self.font)
        font_size = get_arg(font_size, self.font_size)
        text_width_pt = pdfmetrics.stringWidth(text, font, font_size)
        return text_width_pt / mm

    def get_kerning_adjustment(self, prefix, suffix, font, font_size):
        font = get_arg(font, self.font)

        if prefix == "" or suffix == "":
            return 0.0

        kerning_pair = prefix[-1] + suffix[0]
        kerning_table = KERNING.get(font)
        if kerning_table is None:
            return 0.0
        else:
            en_space = font_size / 2 / mm
            result = kerning_table.get(kerning_pair, 0.0) * en_space 
        return result

    def text_bounding_box(self, text, font=None, font_size=None, small_caps=False):
        font_size = get_arg(font_size, self.font_size)
        if small_caps:
            small_font_size = self.small_caps_factor * font_size
            en_space = small_font_size / 2 / mm 
            bbox = Rectangle(0, 0, 0, 0)
            words = text.split()
            for word in text.split():
                while len(word):
                    upper_prefix, word = Page._get_small_caps_upper_prefix(word)
                    if upper_prefix:
                        kerning_adjustment = self.get_kerning_adjustment(upper_prefix, word, font, font_size)
                        word_bbox = self.text_bounding_box(upper_prefix, font=font, font_size=font_size)
                        word_bbox.x = bbox.x2 + kerning_adjustment
                        bbox = bbox.union(word_bbox)
                    
                    lower_prefix, word = Page._get_small_caps_lower_prefix(word)
                    if lower_prefix:
                        word_bbox = self.text_bounding_box(lower_prefix.upper(), font=font, font_size=small_font_size)
                        word_bbox.x = bbox.x2
                        bbox = bbox.union(word_bbox)

            bbox.w += (len(words) - 1) * en_space
            return bbox

        text_height = self.font_height(font=font, font_size=font_size)
        text_width = self.text_width(text, font=font, font_size=font_size)
        if get_arg(font, self.font).startswith("Souvenir"):
            text_height *= 0.6 
        return Rectangle(0, 0, text_width, text_height)

    def register_font(self, path, name):
        path = os.path.expanduser(self.font_path +  "/" + path)
        pdfmetrics.registerFont(TTFont(name, path))

    def register_font_family(self, name, normal=None, bold=None, italic=None):
        pdfmetrics.registerFontFamily(name, normal=normal, bold=bold, italic=italic)

    def set_font(self, name):
        self.font = name

    def draw_text_centered(self, rect, text):
        text_width_pt = pdfmetrics.stringWidth(text, self.font, self.font_size)
        face = pdfmetrics.getFont(self.font).face
        text_height_pt = (face.ascent) / 1000 * self.font_size

        #text_height_pt = self.font_size
        text_size_pt = Point(text_width_pt, text_height_pt)
        center_pt = rect.center() * mm
        pos_pt = center_pt - text_size_pt * 0.5
        self.c.setFont(self.font, self.font_size)
        self.c.drawString(pos_pt.x, pos_pt.y, text)

    def draw_text_aligned(self, text, rect, horizontal_align="center", vertical_align="center", font=None, font_size=None, small_caps=False, color=0.0, horizontal_gap=0, vertical_gap=0):
        text = str(text)
        bbox = self.text_bounding_box(text, font=font, font_size=font_size, small_caps=small_caps)
        bbox = bbox.align_to_rect(rect, horizontal_align, vertical_align, horizontal_gap=horizontal_gap, vertical_gap=vertical_gap)
        self.draw_text(bbox.pos, text, font=font, font_size=font_size, small_caps=small_caps, color=color)
        return bbox.copy()

    def layout_text_aligned(self, text, rect, font=None, font_size=None, min_font_size=6, line_spacing=1.2, horizontal_align="center", vertical_align="center", auto_fit=True):
        """
        Draw multi-line text within a specified rectangle on the ReportLab canvas.
        Automatically reduces the font size until the text fits within the rectangle.
        
        :param c: ReportLab canvas object.
        :param text: The multi-line string to draw.
        :param rectangle: Tuple (x, y, width, height) defining the rectangle in points.
        :param font_name: Name of the registered font to use.
        :param. font_size: Initial font size to attempt.
        :param min_font_size: Minimum font size to reduce to if necessary.
        :param line_spacing: Multiplier for line spacing (default is 1.2).
        :return: The font size used to fit the text.
        """
        font = self.font if font is None else font
        font_size = self.font_size if font_size is None else font_size
        current_font_size = font_size
        
        # Replace newline characters with <br/> tags for Paragraph
        formatted_text = text.replace('\n', '<br/>')

        while current_font_size >= min_font_size:
            # Define a ParagraphStyle
            style = ParagraphStyle(
                name='AutoFitStyle',
                fontName=font,
                fontSize=current_font_size,
                leading=current_font_size * line_spacing,
            )
            
            # Create a Paragraph object
            para = Paragraph(formatted_text, style)
            # Wrap the paragraph to calculate its width and height
            wrap_height = rect.h * mm if auto_fit == True else 0
            para_width, para_height = para.wrap(rect.w * mm, wrap_height)
            para_width /= mm
            para_height /= mm

            lines = text.split("\n")
            max_width = -1
            for line in lines:
                line_width = pdfmetrics.stringWidth(line, font, current_font_size) / mm
                line_width = min(line_width, rect.w)
                max_width = max(line_width, max_width)
            para_width = max_width 

            if para_height <= rect.h or auto_fit == False:
                # Text fits within the rectangle, draw it
                break

            # Text does not fit, reduce the font size and try again
            current_font_size -= 0.5  # Decrease font size by 0.5 points
        
        # If text still doesn't fit, draw it with the minimum font size
        para_rect = Rectangle(0, 0, para_width, para_height).align_to_rect(rect, horizontal_align=horizontal_align, vertical_align=vertical_align)
        para_rect *= mm
        para.drawOn(self.c, para_rect.x, para_rect.y)
        para_rect /= mm
        return para_rect.copy()


    def draw_line(self, line, stroke_color=None, stroke_width=None):
        if stroke_color == None:
            stroke_color = self.stroke_color
        self.c.setStrokeGray(stroke_color)
        if stroke_width == None:
            stroke_width = self.stroke_width
        self.c.setLineWidth(stroke_width)
        self.c.line(line.p1.x * mm, line.p1.y * mm, line.p2.x * mm, line.p2.y * mm)

    def draw_circle(self, pos, radius, stroke_color=None, stroke_width=None):
        if stroke_color == None:
            stroke_color = self.stroke_color
        self.c.setStrokeGray(stroke_color)
        if stroke_width == None:
            stroke_width = self.stroke_width
        self.c.setLineWidth(stroke_width)
        self.c.circle(pos.x * mm, pos.y * mm, radius * mm, fill=0, stroke=1)

    def draw_arc(self, pos, radius, start_angle, end_angle, stroke_color=None, stroke_width=None):
        stroke_color = get_arg(stroke_color, self.stroke_color)
        stroke_width = get_arg(stroke_width, self.stroke_width)
        self.c.saveState()
        self.c.setStrokeGray(stroke_color)
        self.c.setLineWidth(stroke_width)
        x1 = pos.x - radius
        x2 = pos.x + radius
        y1 = pos.y - radius
        y2 = pos.y + radius
        self.c.arc(x1*mm, y1*mm, x2*mm, y2*mm, start_angle, end_angle) 
        self.c.restoreState() 


    def draw_dot(self, pos, lightness=0):
        x = pos.x * mm
        y = pos.y * mm
        self.c.setFillGray(lightness)
        self.c.circle(x, y, 0.5, fill=1, stroke=0)

    @staticmethod
    def adjust_stroke_color(drawing, new_color):
        """
        Recursively adjust strokeColor for shapes within the drawing.
        
        :param drawing: The ReportLab drawing object.
        :param new_color: A ReportLab color instance with desired stroke color and alpha.
        """
        # If the drawing has a 'contents' attribute, iterate through child elements
        if hasattr(drawing, 'contents'):
            for shape in drawing.contents:
                Page.adjust_stroke_color(shape, new_color)  # Recurse into nested shapes
        # If the shape itself supports strokeColor, modify it
        if hasattr(drawing, 'strokeColor'):
            drawing.strokeColor = new_color

    def draw_svg(self, filename, rect, keep_aspect_ratio=True, stroke_color=None):
        svg = svg2rlg(filename)

        # Calculate aspect ratio-preserving scale
        scale_x = rect.w * mm / svg.width
        scale_y = rect.h * mm / svg.height

        # Use the smaller scale to ensure the entire SVG fits
        scale = min(scale_x, scale_y)

        # Scale the SVG
        svg.width *= scale
        svg.height *= scale
        svg.scale(scale, scale)

        if stroke_color:
            color = Color(stroke_color, stroke_color, stroke_color)
            Page.adjust_stroke_color(svg, color)

        # Calculate centered position (optional)
        x = rect.x * mm + (rect.w * mm - svg.width) / 2  # Horizontal centering
        y = rect.y * mm + (rect.h * mm - svg.height) / 2  # Vertical centering

        # Draw the SVG onto the canvas
        renderPDF.draw(svg, self.c, x, y)

    
    def draw_image(self, img, rect, background_color=(255,255,255),flip_vertically=False,rotate=False, rotate_to_fit=False, gray_scale=True, contrast_enhance=2.0, crop=None):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
            tmp_filename = tmp.name
            if isinstance(img, str):
                filename = img
                img = Image.open(img)
            else:
                filename = tmp_filename

            img = crop_transparent_pixels(img)
            img_w, img_h = img.size

            if crop:
                left_crop, right_crop, top_crop, bottom_crop = crop
                img = img_tools.crop(img, left_crop, right_crop, top_crop, bottom_crop) 
                filename = tmp_filename
            
            if rotate_to_fit and (img_w > img_h) != (rect.w > rect.h):
                rotate = True

            if flip_vertically == True:
                img = img_tools.flip_vertically(img)
                filename = tmp_filename

            if rotate:
                img = img_tools.rotate(img)
                filename = tmp_filename

            if img.mode == "RGBA":
                with Image.new("RGB", img.size, background_color) as background:
                    background.paste(img, mask=img.split()[3])
                    img = background
                    filename = tmp_filename
            
            if gray_scale:
                img = img_tools.enhance_contrast(img, contrast_enhance)
                img = img_tools.equalize(img)
                filename = tmp_filename


            if filename == tmp_filename:
                img.save(filename)

            self.c.drawImage(filename, rect.x*mm, rect.y*mm, width=rect.w*mm, height=rect.h*mm, preserveAspectRatio=True)

    def draw_bezier(self, p1, p2, p3, p4, stroke_width=None, stroke_color=None):
        self._set_stroke_style(stroke_width=stroke_width, stroke_color=stroke_color)
        self.c.bezier(p1.x * mm, p1.y * mm, p2.x * mm, p2.y * mm, p3.x * mm, p3.y * mm, p4.x * mm, p4.y * mm)

    def draw_line_humanized(self, line, stroke_width=None, stroke_color=None, num_strokes=3, curvature_spread=0.1, point_spread=0.25):
        for i in range(num_strokes):
            start = line.p1 + point_spread * Point.random_direction() 
            end = line.p2 + point_spread * Point.random_direction() 
            control = line.center_point() + curvature_spread * Point.random_direction()
            self.draw_bezier(start, control, control, end, stroke_width=stroke_width, stroke_color=stroke_color)

    def draw_rect_humanized(self, rect, stroke_width=None, stroke_color=None, num_strokes=2, curvature_spread=0.2, point_spread=0.25):
        for e in rect.edges():
            self.draw_line_humanized(e, stroke_width=stroke_width, stroke_color=stroke_color, num_strokes=num_strokes, curvature_spread=curvature_spread, point_spread=point_spread)


    def subdivide(self, rows, cols):
        rects = self.page_rect.subdivide(rows, cols)
        for r in rects:
            self.draw_rect(r)
        return rects

    def is_landscape(self):
        return self.pagesize[0] > self.pagesize[1]

    def toggle_landscape(self):
        w, h = self.pagesize
        self.set

    def new_page(self, landscape=None):
        self.c.showPage()
        if landscape is not None:
            if landscape:
                self.set_pagesize(pagesizes.landscape(self.pagesize))
            else:
                self.set_pagesize(pagesizes.portrait(self.pagesize))


    def save(self):
        self.c.save()

    def push_state(self):
        self.state_stack.append(copy.deepcopy(self.state))

    def pop_state(self):
        self.state_stack.pop()

    def _set_stroke_style(self, stroke_color=None, stroke_width=None): 
        self.c.setStrokeGray(self.stroke_color if stroke_color == None else stroke_color)
        self.c.setLineWidth(mm*(self.stroke_width if stroke_width == None else stroke_width))

    def draw_cut_marks(self, rects, length=10, gap=2):
        self.stroke_width = 0.25
        self.stroke_color = 0.75
        x1, y1 = 1e9, 1e9
        x2, y2 = -1e9, -1e9
        for r in rects:
            x1 = min(x1,r.x1)
            y1 = min(y1,r.y1)
            x2 = max(x2,r.x2)
            y2 = max(y2,r.y2)

        horizontal_marks = set([ r.y1 for r in rects ] + [ r.y2 for r in rects ])
        vertical_marks = set([ r.x1 for r in rects ] + [ r.x2 for r in rects ])

        [self.draw_line(Line(Point(x1 - gap - length, y), Point(x1 - gap, y))) for y in horizontal_marks ]
        [self.draw_line(Line(Point(x2 + gap, y), Point(x2 + gap + length, y))) for y in horizontal_marks ]

        [self.draw_line(Line(Point(x, y1 - gap - length), Point(x, y1 - gap))) for x in vertical_marks ]
        [self.draw_line(Line(Point(x, y2 + gap), Point(x, y2 + gap + length))) for x in vertical_marks ]

    def push_layout_rect(self, rect, draw_func):
        self.layout_rect_list.append((rect, draw_func))

    def get_min_height_layout_rect(self):
        if len(self.layout_rect_list):
            return sorted(
                self.layout_rect_list,
                key=lambda item: item[0].h)[0]
        else:
            return None

    def get_min_width_layout_rect(self):
        if len(self.layout_rect_list):
            return sorted(
                self.layout_rect_list,
                key=lambda item: item[0].w)[0]
        else:
            return None

    def _keep_free_rect(self, rect):
        for r,_ in self.layout_rect_list:
            if rect.w >= r.w and rect.h >= r.h:
                return True
        return False


    def _find_layout_rect_for_free_rect(self, free_rect):
        for i,item in enumerate(self.layout_rect_list):
            r = item[0]
            if r.w <= free_rect.w and r.h <= free_rect.h:
                del self.layout_rect_list[i]
                return item
        return None


    def place_bbox(self, union_rect, bbox):
        if bbox.w + union_rect.x2 > self.drawable_rect.x2:
            pos = union_rect.bottom_left()
            union_rect = Rectangle(pos.x, pos.y, 0, 0)

        if union_rect.y2 - bbox.h < self.drawable_rect.y1:
            self.new_self()
            union_rect = Rectangle(self.drawable_rect.x1, self.drawable_rect.y2, 0, 0)

        pos = union_rect.top_right()
        bbox = bbox.translate(pos - Point(0, bbox.h))
        union_rect = union_rect.union(bbox)

        return union_rect, bbox
        
    def perform_layout(self, rows_first=True):
        free_rects = [self.drawable_rect]
        self.layout_rect_list.sort(key=lambda item: item[0].h, reverse=True)
        while self.layout_rect_list:
            if not free_rects:
                self.new_page()
                free_rects.insert(0, self.drawable_rect)
            free_rect = free_rects.pop(0)
            item = self._find_layout_rect_for_free_rect(free_rect)
            if item is not None:
                draw_rect, draw_func = item
                draw_rect = draw_rect.align_to_rect(free_rect, "left", "top")
                draw_func(self, draw_rect)
                above_rect, below_rect = free_rect.top_partition(height=draw_rect.h)
                _, right_rect = above_rect.left_partition(width=draw_rect.w)
                free_rects.insert(0,below_rect)
                free_rects.insert(0,right_rect)

    def perform_layout_columns_first(self):
        free_rects = [self.drawable_rect]
        self.layout_rect_list.sort(key=lambda item: item[0].w, reverse=True)
        while self.layout_rect_list:
            if not free_rects:
                self.new_page()
                free_rects.insert(0, self.drawable_rect)
            free_rect = free_rects.pop(0)
            item = self._find_layout_rect_for_free_rect(free_rect)
            if item is not None:
                draw_rect, draw_func = item
                draw_rect = draw_rect.align_to_rect(free_rect, "left", "top")
                draw_func(self, draw_rect)
                left_rect, right_rect = free_rect.left_partition(width=draw_rect.w)
                _, below_rect = left_rect.top_partition(height=draw_rect.h)
                free_rects.insert(0,right_rect)
                free_rects.insert(0,below_rect)
