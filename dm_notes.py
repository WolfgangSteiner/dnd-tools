from pdf_tools import Page, Rectangle



class PageTemplate:
    def __init__(
        self,
        page,
        horizontal_margin=20,
        vertical_margin=20,
        column_gap=5
    ):
        self.page = page
        self.content_rect = page.page_rect.apply_margin(horzontal_margin, vertical_margin)
        self.left_column, self.right_column = self.content_rect.left_partition(0.5, gap=column_gap)
        self.current_column = self.left_column


def draw_note(page, rect, title, text):
    heading_rect, body = rect.top_partition(height = 10, gap=2)
    page.draw_text_aligned(title, heading_rect, "left", "center", font="RobotoSlabBold")
    page.layout_text_aligned(text, body, font="Times-Roman", horizontal_align="left", vertical_align="top")
    

page = Page("pdf/dm_notes.pdf", pagesize=Page.A4, landscape=True)
pt = PageTemplate(page)

rects = page.page_rect.apply_margin(20,20).subdivide(1,3)


notes = [
    ("Letter from Gundren", "I hope you are well. I have finally found the missing link to locating the Key to the Forge of Spells! The Key lies in the Tomb of Diras, of course! He was one of the few survivers of the Wave Echo Cave! Travel to ")]

for i,note in enumerate(notes):
    draw_note(page, rects[i%3], note[0], note[1])
    if i % 3 == 2:
        page.new_page()



page.save()
