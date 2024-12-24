from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from dnd_map import Rect

c = canvas.Canvas("spell_cards.pdf", pagesize=A4)
page_rect = Rect.from_canvas(c, margin=0)

rects = page_rect.subdivide(3,3)

def draw_cross(canvas, pos, size=2):
    x1 = pos.x - size / 2
    x2 = pos.x + size / 2
    y1 = pos.y - size / 2
    y2 = pos.y + size / 2
    canvas.line(x1*mm, pos.y*mm, x2*mm, pos.y*mm)
    canvas.line(pos.x*mm, y1*mm, pos.x*mm, y2*mm)


def draw_backside(canvas, rect):
    rect.fill(canvas, 0.5, radius=5)

for r in rects:
    c.setStrokeGray(0.8)
    c.setLineWidth(1)
    r.draw(c)
    

spells = ["Light", "Fire Bolt", "Burning Hands", "Detect Magic", "Expeditious Retreat", "False Life", "Magic Missile", "Ray of Frost", "Sleep"]
for i, spell in enumerate(spells):
    spell = spells[i]
    r = rects[i]
    p = r.center()
    c.drawString(p.x*mm, p.y*mm, str(i))
    c.drawImage(f"spell_cards/{spell}.png", r.x*mm, r.y*mm, width=r.w*mm, height=r.h*mm, preserveAspectRatio=True)

c.showPage()
for r in rects:
    c.setStrokeGray(0.8)
    c.setLineWidth(0.5)
    r = r.apply_margin(5, 5)
    r.draw(c)


c.save()
