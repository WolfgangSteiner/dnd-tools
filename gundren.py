from dnd_tools import Character

gundren = Character(
    name="Gundren Rockseeker", level=2, ancestry="Mountain Dwarf", profession="Miner",
    background="Guild Artisan",
    str=13, dex=10, con=14, int=12, wis=11, cha=13,
    skills=["history", "insight", "persuation", "athletics"],
    saving_throws=["int", "wis"],
    gp=10,
    ini=1, ac=13, max_hp=15, hit_dice="2d8", spd=25)

gundren.attacks = [
    "Miner's Pick|+3|1d8+1",
    "Light Hammer (R) | +2 | 1d4+1",
]

gundren.proficiencies = [
    "Light Armor",
    "Simple Weapons",
    "Miner's Pick",
    "Hammers",
    "Shields",
]

gundren.feats_traits = [
    "Darkvision",
    "Dwarven Resilience",
    "Stonecunning",
    "Guild Membership",
]

gundren.gear = [
    "Leather Armor",
    "Miner's Pick",
    "Shield",
]

gundren.backpack = [
    "Bedroll",
    "Lantern",
    "10 Pints of Oil",
    "10 Rations",
    "Hammer",
    "Pitons",
    "50ft Rope",
]

gundren.items = [
    "Diary",
    "Map to Wave Echo Cave",
    "Ink & Pen",
]

gundren.personality = "I am always thinking about the next vein of ore to strike it rich."
gundren.ideals = r"It's he duty of every guild member to strengthen and protect the community."
gundren.bonds = "Discovering the Wave Echo Cave is my life's ambition."
gundren.flaws = "I will get overconfident when it comes to mining ventures."
