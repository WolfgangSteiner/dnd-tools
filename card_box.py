from pdf_tools import Page, Rectangle, Line
import typer


class Group:
    def __init__(self):
        self.objects = []

    def add_rect(self, rect):
        self.objects.append(rect)
        return rect

    def align_to_previous(self, rect, horizontal_align, vertical_align, idx=-1):
        rect = rect.align_to_rect(self.objects[idx], horizontal_align, vertical_align)
        self.objects.append(rect)
        return rect


def main(
    width:int,
    height:int,
    thickness:int,
    paper_thickness:int=1,
    padding:int=1,
    flap_height:int=15,
    glue_flap_width:int=15,
):
    page = Page("pdf/card_box.pdf", landscape=True)
    rects = []
    g = Group()
    total_width = width + padding + paper_thickness
    total_height = height + padding
    total_thickness = thickness + paper_thickness + padding
    back_rect = g.add_rect(Rectangle(w=total_width, h=total_height))
    g.align_to_previous(Rectangle(w=total_thickness), "right_of", "block")
    g.align_to_previous(Rectangle(h=width*0.3), "block", "above")
    g.align_to_previous(Rectangle(h=width*0.3), "block", "below", -2)
    front_rect = g.align_to_previous(Rectangle(w=total_width), "right_of", "block", -3)
    g.align_to_previous(Rectangle(w=total_thickness-2), "right_of", "block")
    g.align_to_previous(Rectangle(h=total_thickness), "block", "below", -2)
    g.align_to_previous(Rectangle(h=glue_flap_width), "block", "below")
    g.align_to_previous(Rectangle(h=total_thickness), "block", "above", 0)
    g.align_to_previous(Rectangle(h=flap_height), "block", "above")
    g.align_to_previous(Rectangle(w=total_thickness), "left_of", "block", 0)
    g.align_to_previous(Rectangle(h=width*0.3), "block", "above")
    g.align_to_previous(Rectangle(h=width*0.3), "block", "below", -2)
    g.align_to_previous(Rectangle(h=10), "block", "top", 0)

    rects = Rectangle.align_rects_to_rect(g.objects, page.drawable_rect, "left", "top")
    
    for r in rects:
        page.draw_rect(r, stroke_width=0.25, stroke_color=0.75)
    page.draw_arc(rects[4].top_center(), 10, 180, 180, stroke_width=0.25, stroke_color=0.75)

    page.save()


if __name__ == "__main__":
    typer.run(main)
