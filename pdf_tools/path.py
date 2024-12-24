from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from .line import Line

class Path:
    def __init__(self, points=None):
        self.points = points if points else []
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

    def get_lines(self):
        res = []
        for i in range(len(self.points) - 1):
            res.append(Line(self.points[i], self.points[i+1]))
        return res
    
    def merge_path(self, path):
        for p in path.points:
            self.points.append(p)

