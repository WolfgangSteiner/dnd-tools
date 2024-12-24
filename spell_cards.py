from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pdf_tools import Page,Rectangle,Point


p = Page("pdf/spell_cards.pdf")
page_rect = p.page_rect()

rects = p.subdivide(3,3)

def draw_cross(canvas, pos, size=2):
    x_off = Point(size / 2, 0)
    x_off = Point(0, size / 2)
    p.draw_line(Line(pos - x_off, pos + x_off))
    p.draw_line(Line(pos - y_off, pos + y_off))

def draw_backside(canvas, rect):
    rect.fill(canvas, 0.5, radius=5)


spells_t = ["Light", "Fire Bolt", "Burning Hands", "Detect Magic", "Expeditious Retreat", "False Life", "Magic Missile", "Ray of Frost", "Sleep"]

spells_cleric_lv1 = ["Bane", "Bless", "Command", "Create or Destroy Water", "Cure Wounds", "Detect Evil and Good", "Detect Magic", "Detect Poison and Disease", "Guiding Bolt", "Healing Word", "Inflict Wounds", "Protection from Evil and Good", "Purify Food and Drink", "Sanctuary", "Shield of Faith"]

spells_cleric_cantrip = ["Guidance", "Light", "Mending", "Resistance", "Sacred Flame", "Spare the Dying", "Thaumaturgy"]

spells = spells_cleric_lv1 + spells_cleric_cantrip

for i, spell in enumerate(spells):
    spell = spells[i]
    r = rects[i%9]
    p.draw_image(f"spell_cards/{spell}.png", r)
    if i%9 == 8:
        p.new_page()
        p.subdivide(3,3)

#c.showPage()
#for r in rects:
#    c.setStrokeGray(0.8)
#    c.setLineWidth(0.5)
#    r = r.apply_margin(5, 5)
#    r.draw(c)


p.save()
