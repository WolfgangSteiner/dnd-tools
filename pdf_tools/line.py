from .point import Point


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @staticmethod
    def from_center_and_width(center, width):
        return Line(center - Point(width / 2,0), center + Point(width / 2, 0))

    def center_point(self):
        return 0.5 * (self.p1 + self.p2)
