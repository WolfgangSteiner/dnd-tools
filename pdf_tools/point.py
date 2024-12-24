import math
import random

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

    def inc_x(self, ox):
        return Point(self.x + ox, self.y)

    def inc_y(self, oy):
        return Point(self.x, self.y + oy)

    @staticmethod
    def random_direction():
        phi = 2*math.pi * random.random()
        return Point(math.cos(phi), math.sin(phi))
        
