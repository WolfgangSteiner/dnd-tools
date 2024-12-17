import copy

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
