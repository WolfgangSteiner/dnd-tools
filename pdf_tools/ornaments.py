from .page import Page
from .rectangle import Rectangle
from types import SimpleNamespace

def _draw_corner(page, path, cfg=SimpleNamespace()):
    for l in path.get_lines():
        page.draw_line_humanized(l,
            stroke_width=getattr(cfg, "stroke_width", None),
            stroke_color=getattr(cfg, "stroke_color", None),
            num_strokes=getattr(cfg, "num_strokes", 3),
            curvature_spread=getattr(cfg, "curvature_spread", 0.1),
            point_spread=getattr(cfg, "point_spread", 0.25)
        )

def draw_rect_corners_humanized(page, rect, cfg=SimpleNamespace()):
    corner_width = getattr(cfg, "corner_width", None)
    corner_fraction = getattr(cfg, "corner_fraction", 0.25)
    for c in ("top_left", "top_right", "bottom_left", "bottom_right"):
        path = rect.get_corner_path(c, fraction=corner_fraction, width=corner_width)
        _draw_corner(page, path, cfg)
