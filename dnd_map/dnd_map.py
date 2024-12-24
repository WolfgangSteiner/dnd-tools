import copy
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

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
        canvas.drawPath(path, stroke=1, fill=1)

    def merge_path(self, path):
        for p in path.points:
            self.points.append(p)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def x2(self):
        return self.x + self.w

    def y2(self):
        return self.y + self.h

    def align_to_rect(self, rect, horizontal_align="center", vertical_align="center"):
        res = Rect(self.x, self.y, self.w, self.h)
        if horizontal_align == "center":
            res.x = rect.x + (rect.w - self.w) / 2
        elif horizontal_align == "left":
            res.x = rect.x
        elif horizontal_align == "right":
            res.x = rect.x + rect.w - res.w
        elif horizontal_align == "block":
            res.x = rect.x
            res.w = rect.w
        else:
            raise ValueError

        if vertical_align == "center":
            res.y = rect.y + (rect.h - self.h) / 2
        elif vertical_align == "top":
            res.y = rect.y + rect.h - res.y
        elif vertical_align == "bottom":
            res.y = rect.y
        elif vertical_align == "block":
            res.y = rect.y
            res.h = rect.h
        else:
            raise ValueError

        return res


    def apply_margin(self, mx, my):
        return Rect(self.x + mx, self.y + my, self.w - 2*mx, self.h - 2*my)

    def subdivide(self, num_rows, num_columns):
        w = self.w / num_columns
        h = self.h / num_rows
        res = []
        for row in range(0, num_rows):
            for col in range(0, num_columns):
                res.append(Rect(col * w + self.x, row * h + self.y, w, h))

        return res

    def draw(self, canvas, width=None, hue=None):
        if width is not None:
            canvas.setLineWidth(width*mm)
        if hue is not None:
            canvas.setStrokeGray(hue)
        canvas.rect(self.x * mm, self.y * mm, self.w * mm, self.h * mm, stroke=1, fill=0)


    def fill(self, canvas, hue, radius=0.0):
        if radius == 0.0:
            canvas.rect(self.x*mm, self.y*mm, self.w*mm, self.h*mm, stroke=0, fill=1)
        else:
            canvas.setFillGray(hue)
            canvas.roundRect(self.x*mm, self.y*mm, self.w*mm, self.h*mm, radius=radius *mm, stroke=0, fill=1)

    def corners(self):
        return [
            Point(self.x, self.y), 
            Point(self.x + self.w, self.y), 
            Point(self.x + self.w, self.y + self.h), 
            Point(self.x, self.y + self.h)] 

    def center(self):
        return Point(self.x + self.w / 2, self.y + self.h / 2)


    @staticmethod
    def from_canvas(canvas, margin=5):
        return Rect(0, 0, canvas._pagesize[0] / mm, canvas._pagesize[1] / mm).apply_margin(margin, margin)

