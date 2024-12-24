import copy
from .path import Path

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

    def draw(self, page):
        for p in self.paths:
            p.draw(page)

