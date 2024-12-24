from pdf_tools import Page, Rectangle


page = Page("pdf/daily_goals_cards.pdf", landscape=True)

def draw_goal_grid(page, rect, num_rows, num_cols, grid_size=3):
    content_rect = Rectangle(0, 0, num_cols * grid_size, num_rows * grid_size)
    content_rect = content_rect.align_to_rect(rect)
    for r in content_rect.subdivide(num_rows, num_cols):
        page.draw_rect(r)


for r in page.subdivide(4,4):
    r = r.apply_margin(10,5)
    for cr in r.subdivide(1,3):
        draw_goal_grid(page, cr, 4, 4)

page.new_page()

for r in page.subdivide(2,4):
    r = r.apply_margin(10,5)
    r.w -= 0
    r.x += 5
    r.h -= 5
    for cr in r.subdivide(7,4):
        draw_goal_grid(page, cr, 4, 4, grid_size=2.5)

page.save()
