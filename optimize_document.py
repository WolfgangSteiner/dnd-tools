from pdf_tools import Page, Rectangle
import glob

page = Page("pdf/tales_of_the_yawning_portal.pdf")

crop=(0.05, 0.0, 0.03, 0.1)

for filepath in glob.glob("assets/tales_of_the_yawning_portal/*01[1-5].jpg"):
    print(filepath)
    page.draw_image(filepath, page.page_rect, contrast_enhance=16.0, crop=None)
    page.new_page()

page.save()


