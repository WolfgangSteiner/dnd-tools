from types import SimpleNamespace

class Style(SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stroke = SimpleNamespace(width=0.5, color=1.0)
        

