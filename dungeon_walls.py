from pdf_tools import Page, Rectangle, Line
import typer

def get_arg(arg, default):
    return default if arg is None else arg

class RectangleGroup:
    def __init__(self, rect=None):
        self.objects = []
        if rect:
            self.objects.append(rect)

    def add(self, rect):
        self.objects.append(rect)
        return rect

    def add_aligned(self, rect, horizontal_align="center", vertical_align="center", idx=-1, align_rect=None):
        align_rect = get_arg(align_rect, self.objects[idx])
        rect = rect.align_to_rect(align_rect, horizontal_align, vertical_align)
        self.objects.append(rect)
        return rect


    def align_to_rect(self,rect, horizontal_align="center", vertical_align="center"):
        self.objects = Rectangle.align_rects_to_rect(self.objects, rect, horizontal_align=horizontal_align, vertical_align=vertical_align)

    def draw(self, page, stroke_width=0.25, stroke_color=0.0):
        for r in self.objects:
            page.draw_rect(r, stroke_width=stroke_width, stroke_color=stroke_color)

    def bounding_box(self):
        if len(self.objects) == 0:
            return Rectangle()
        else:
            bbox = self.objects[0]
            for r in self.objects:
                bbox = bbox.union(r)
        return bbox
        
    def clone(self, horizontal_align="center", vertical_align="center"):
        res = RectangleGroup()
        res.objects = self.objects[:]
        res.align_to_rect(self.bounding_box(), horizontal_align, vertical_align)
        return res

def generate_wall(
    length:int=6*25,
    height:int=50,
    width:int=25,
):
    rg = RectangleGroup(Rectangle(w=length+2*width, h=2*height+width))
    center = rg.add_aligned(Rectangle(w=length, h=width))
    c1 = rg.add_aligned(Rectangle(w=width, h=height), "left_of", "above")
    c2 = rg.add_aligned(c1, "right_of", "above", align_rect=center)
    rg.add_aligned(c1, "left_of", "below", align_rect=center)
    rg.add_aligned(c1, "right_of", "below", align_rect=center)
    rg.add_aligned(Rectangle(h=width/2), "block", "below", align_rect=c1)
    rg.add_aligned(Rectangle(h=width/2), "block", "below", align_rect=c2)
    return rg

def generate_corner(
    length:int=6*25,
    height:int=50,
    width:int=25,
):
    rg = generate_wall(length, height, width)
    r = rg.add_aligned(Rectangle(w=width,h=width), "center", "center", idx=0)
    rg.add_aligned(Rectangle(h=height), "block", "below")
    return rg


def main(
    length:int=6*25,
    height:int=50,
    width:int=25,
    glue_flap_width:int=15,
):
    page = Page()
    rg = generate_wall(length=length, height=height, width=width)
    rg.align_to_rect(page.drawable_rect, "left", "top")        
    rg.draw(page, stroke_color=0.75)

    rg2 = generate_wall(length=length, height=height, width=width)
    rg2.align_to_rect(rg.bounding_box(), "center", "below")        
    rg2.draw(page, stroke_color=0.75)

    page.save()



if __name__ == "__main__":
    typer.run(main)
