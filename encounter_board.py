from pdf_tools import Page, Rectangle
from dnd_tools import Monster


monsters = Monster.load_monsters_from_directory("monsters")
print(monsters['goblin'])

page = Page("pdf/encounter_board.pdf", landscape=True)

page.save()
