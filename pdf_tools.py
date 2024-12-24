from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p2):
        return Point(self.x + p2.x, self.y + p2.y)

    def __sub__(self, p2):
        return Point(self.x - p2.x, self.y - p2.y)

    def __mul__(self, a):
        return Point(self.x * a, self.y * a)

    def __rmul__(self, a):
        return self.__mul__(a)

class Rectangle:
    def __init__(self, x, y, w, h, radius=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.radius = radius

    def center(self):
        return Point(self.x + self.w / 2, self.y + self.h / 2)

    def x1(self):
        return self.x

    def x2(self):
        return self.x + self.w

    def y1(self):
        return self.y

    def y2(self):
        return self.y + self.h


    def align_to_rect(self, r, h_align, v_align):
        res = Rectangle(self.x, self.y, self.w, self.h)
        if h_align == "left":
            res.x = r.x
        elif h_align == "right":
            res.x = r.x2() - res.w
        else:
            raise ValueError

        if v_align == "top":
            res.y = r.y + r.h - res.h
        elif v_align == "bottom":
            res.y = r.y
        else:
            raise ValueError

        return res

    def left_edge(self):
        return Line(Point(self.x1(), self.y1()), Point(self.x1(), self.y2()))

    def right_edge(self):
        return Line(Point(self.x2(), self.y1()), Point(self.x2(), self.y2()))

    def bottom_edge(self):
        return Line(Point(self.x1(), self.y1()), Point(self.x2(), self.y1()))

    def top_edge(self):
        return Line(Point(self.x1(), self.y2()), Point(self.x2(), self.y2()))

    def top_partition(self, factor=1.0, height=0.0):
        if factor != 1.0:
            res = Rectangle(self.x, self.y, self.w, self.h * factor).align_to_rect(self, "left", "top")
        else:
            res = Rectangle(self.x, self.y, self.w, height).align_to_rect(self, "left", "top")
        remain = Rectangle(self.x, self.y, self.w, self.h - res.h).align_to_rect(self, "left", "bottom")
        return res, remain

    def translate(self, p):
        return Rectangle(self.x + p.x, self.y + p.y, self.w, self.h, self.radius)

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class PageInfo:
    def __init__(self, filename, pagesize, margin):
        w, h = pagesize
        self.w = w / mm
        self.h = h / mm
        self.left_margin = margin
        self.right_margin = margin
        self.top_margin = margin
        self.bottom_margin = margin
        self.pagesize = pagesize
        self.stroke_width = 0.25
        self.stroke_color = 0.5
        self.font = "Helvetica"
        self.font_size = 10
        self.c = canvas.Canvas(filename, pagesize=pagesize)

    def draw_rect(self, r):
        self.c.setStrokeGray(self.stroke_color)
        self.c.setLineWidth(self.stroke_width)
        if r.radius:
            self.c.roundRect(r.x * mm, r.y * mm, r.w * mm, r.h * mm, r.radius * mm, stroke = 1, fill = 0)
        else:
            self.c.rect(r.x * mm, r.y * mm, r.w * mm, r.h * mm, stroke=1, fill=0)

    def drawable_rect(self):
        return Rectangle(self.left_margin, self.bottom_margin, self.w - self.left_margin - self.right_margin, self.h - self.bottom_margin - self.top_margin)

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

    def draw_rounded_rect(self, r, radius, stroke_width=None):
        self.c.setStrokeGray(self.stroke_color)
        self.c.setLineWidth(self.stroke_width if stroke_width == None else stroke_width)
        self.c.roundRect(r.x * mm,  r.y * mm, r.w * mm, r.h * mm, radius * mm, stroke = 1, fill = 0)

    def draw_text(self, pos, text):
        face = pdfmetrics.getFont(self.font).face
        self.c.setFont(self.font, self.font_size)
        self.c.drawString(pos.x * mm, pos.y * mm, text)

    def font_height(self):
        face = pdfmetrics.getFont(self.font).face
        return (face.ascent) / 1000 * self.font_size / mm

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

    def draw_line(self, line, stroke_color=None, stroke_width=None):
        if stroke_color == None:
            stroke_color = self.stroke_color
        self.c.setStrokeGray(stroke_color)
        if stroke_width == None:
            stroke_width = self.stroke_width
        self.c.setLineWidth(stroke_width)
        self.c.line(line.p1.x * mm, line.p1.y * mm, line.p2.x * mm, line.p2.y * mm)
