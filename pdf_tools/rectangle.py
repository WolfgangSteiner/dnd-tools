from .point import Point
from .line import Line
from .path import Path

class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0, x1=None, x2=None, y1=None, y2=None, radius=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if x1 is not None:
            self.x = x1
        if y1 is not None:
            self.y = y1
        if x2 is not None:
            self.w = x2 - self.x
        if y2 is not None:
            self.h = y2 - self.y

        self.radius = radius

    @property
    def x1(self):
        return self.x

    @property
    def x2(self):
        return self.x + self.w

    @property
    def y1(self):
        return self.y

    @property
    def y2(self):
        return self.y + self.h

    @property
    def corners(self):
        return [
            Point(self.x, self.y), 
            Point(self.x + self.w, self.y), 
            Point(self.x + self.w, self.y + self.h), 
            Point(self.x, self.y + self.h)] 

    @property
    def pos(self):
        return Point(self.x, self.y) 

    @pos.setter
    def pos(self, value):
        self._pos = value

    def __mul__(self, factor):
        return Rectangle(self.x * factor, self.y * factor, self.w * factor, self.h * factor)

    def top_left(self):
        return Point(self.x1, self.y2)

    def top_right(self):
        return Point(self.x2, self.y2)

    def bottom_left(self):
        return Point(self.x1, self.y1)

    def bottom_right(self):
        return Point(self.x2, self.y1)

    def center(self):
        return Point(self.x + self.w / 2, self.y + self.h / 2)

    def left_edge(self):
        return Line(Point(self.x1, self.y1), Point(self.x1, self.y2))

    def right_edge(self):
        return Line(Point(self.x2, self.y1), Point(self.x2, self.y2))

    def bottom_edge(self):
        return Line(Point(self.x1, self.y1), Point(self.x2, self.y1))

    def top_edge(self):
        return Line(Point(self.x1, self.y2), Point(self.x2, self.y2))

    def edges(self):
        return [self.bottom_edge(), self.right_edge(), self.top_edge(), self.left_edge()]

    def align_to_rect(self, rect, horizontal_align="center", vertical_align="center", horizontal_gap=0, vertical_gap=0):
        res = Rectangle(self.x, self.y, self.w, self.h)
        res = res.horizontal_align_to_rect(rect, align=horizontal_align, gap=horizontal_gap)
        res = res.vertical_align_to_rect(rect, align=vertical_align, gap=vertical_gap)
        return res

    def horizontal_align_to_rect(self, rect, align="center", gap=0):
        res = Rectangle(self.x, self.y, self.w, self.h)
        if align in ("center", "c"):
            res.x = rect.x + (rect.w - self.w) / 2
        elif align in ("left", "l"):
            res.x = rect.x
        elif align in ("right", "r"):
            res.x = rect.x + rect.w - res.w
        elif align == "block":
            res.x = rect.x
            res.w = rect.w
        elif align == "left_of":
            res.x = rect.x - res.w - gap
        elif align == "right_of":
            res.x = rect.x2 + gap
        else:
            raise ValueError

        return res

    def vertical_align_to_rect(self, rect, align="center", gap=0):
        res = Rectangle(self.x, self.y, self.w, self.h)
        if align == "center":
            res.y = rect.y + (rect.h - self.h) / 2
        elif align == "top":
            res.y = rect.y2 - res.h
        elif align == "bottom":
            res.y = rect.y
        elif align == "block":
            res.y = rect.y
            res.h = rect.h
        elif align == "above":
            res.y = rect.y2 + gap 
        elif align == "below":
            res.y = rect.y1 - res.h - gap
        else:
            raise ValueError

        return res

    def apply_margin(self, mx, my):
        return Rectangle(self.x + mx, self.y + my, self.w - 2*mx, self.h - 2*my)

    def apply_margin_left(self, m):
        return Rectangle(self.x + m, self.y, self.w - m, self.h)

    def apply_margin_right(self, m):
        return Rectangle(self.x, self.y, self.w - m, self.h)

    def apply_margin_leftright(self, m):
        return Rectangle(self.x + m, self.y, self.w - 2*m, self.h)

    def apply_margin_top(self, m):
        return Rectangle(self.x, self.y, self.w, self.h - m)

    def apply_margin_bottom(self, m):
        return Rectangle(self.x, self.y + m, self.w, self.h - m)

    def scale_to_width(self, w):
        return Rectangle(self.x, self.y, w, self.h / self.w * w)

    @staticmethod
    def _compute_subdivide_factors(elements):
        if isinstance(elements, (list, tuple)):
            total = sum(elements)
            return [ e / total for e in elements ]
        else:
            return [ 1 / elements for i in range(elements) ]
    
    def union(self, rect):
        x1 = min(self.x1, rect.x1)
        y1 = min(self.y1, rect.y1)
        x2 = max(self.x2, rect.x2)
        y2 = max(self.y2, rect.y2)
        return Rectangle(x1, y1, x2 - x1, y2 - y1) 

    def copy(self):
        return Rectangle(self.x, self.y, self.w, self.h)

    def subdivide(self, rows, columns, horizontal_gap=0, vertical_gap=0, col_wise=False):
        row_factors = Rectangle._compute_subdivide_factors(rows)
        column_factors = Rectangle._compute_subdivide_factors(columns)
        res = []
        y = self.y + self.h
        available_height = self.h - (vertical_gap * (len(row_factors) - 1))
        available_width = self.w - (horizontal_gap * (len(column_factors) - 1))
        for row_factor in row_factors:
            h = row_factor * available_height
            y -= h
            x = self.x
            for column_factor in column_factors:
                w = column_factor * available_width 
                res.append(Rectangle(x, y, w, h))
                x += w + horizontal_gap
            y -= vertical_gap
        
        if col_wise:
            res_colwise = []
            for col in range(columns):
                for row in range(rows):
                    res_colwise.append(res[row*columns+col])
            return res_colwise

        return res

    def top_partition(self, factor=1.0, height=0.0, gap=0):
        if factor != 1.0:
            res = Rectangle(self.x, self.y, self.w, (self.h - gap) * factor).align_to_rect(self, "left", "top")
        else:
            res = Rectangle(self.x, self.y, self.w, height).align_to_rect(self, "left", "top")
        remain = Rectangle(self.x, self.y, self.w, self.h - res.h - gap).align_to_rect(self, "left", "bottom")
        return res, remain

    def bottom_partition(self, factor=1.0, height=0.0, gap=0):
        bottom_h = (self.h - gap) * factor if factor != 1.0 else height
        bottom = Rectangle(0, 0, self.w, bottom_h).align_to_rect(self, "block", "bottom")
        top = Rectangle(0, 0, self.w, self.h - bottom.h - gap).align_to_rect(self, "block", "top")
        return top, bottom

    def left_partition(self, factor=1.0, width=0.0, gap=0):
        if factor != 1.0:
            res = Rectangle(self.x, self.y, (self.w - gap) * factor, self.h).align_to_rect(self, "left", "top")
        else:
            res = Rectangle(self.x, self.y, width, self.h).align_to_rect(self, "left", "top")
        remain = Rectangle(self.x, self.y, self.w - res.w - gap, self.h).align_to_rect(self, "right", "top")
        return res, remain

    def right_partition(self, factor=1.0, width=0.0, gap=0):
        if factor != 1.0:
            res = Rectangle(self.x, self.y, (self.w - gap) * factor, self.h).align_to_rect(self, "right", "top")
        else:
            res = Rectangle(self.x, self.y, width, self.h).align_to_rect(self, "right", "top")
        remain = Rectangle(self.x, self.y, self.w - res.w - gap, self.h).align_to_rect(self, "left", "top")
        return remain, res

    def translate(self, p):
        return Rectangle(self.x + p.x, self.y + p.y, self.w, self.h, self.radius)

    def get_corner_path(self, name, fraction=0.25, width=None):
        if width is None:
            w = self.w * fraction
            h = self.h * fraction
            width = min(w, h)
        name = name.replace("-", "_")
        name = name.replace(" ", "_")
        if name == "top_left":
            p2 = self.top_left()
            p1 = p2 - Point(0, width)
            p3 = p2 + Point(width, 0)
        elif name == "top_right":
            p2 = self.top_right()
            p1 = p2 - Point(0, width)
            p3 = p2 - Point(width, 0)
        elif name == "bottom_right":
            p2 = self.bottom_right()
            p1 = p2 + Point(0, width)
            p3 = p2 - Point(width, 0)
        elif name == "bottom_left":
            p2 = self.bottom_left()
            p1 = p2 + Point(0, width)
            p3 = p2 + Point(width, 0)
        else:
            raise ValueError

        return Path([p1,p2, p3])

    def make_grid(self, width, height, horizontal_align="left", vertical_align="top"):
        num_cols = self.w // width
        num_rows = self.h // height
        bbox = Rectangle(0,0,num_cols*width,num_rows*height).align_to_rect(self, horizontal_align=horizontal_align, vertical_align=vertical_align)
        return bbox, bbox.subdivide(int(num_rows), int(num_cols))
        
        



