from pdf_tools import Page, Rectangle
import glob

page = Page("pdf/dragon_of_icespire_peak.pdf")

crop=(0.05, 0.0, 0.03, 0.1)

for filepath in glob.glob("assets/dragon_of_icespire_peak/*.jpg"):
    print(filepath)
    page.draw_image(filepath, page.page_rect, contrast_enhance=2.0, crop=None)
    page.new_page()

page.save()


