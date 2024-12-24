from dnd_tools import Character

orikour = Character(
    name="Orikour Whiteforge", level=2, ancestry="Mountain Dwarf", profession="Barbarian",
    str=16, dex=14, con=16, int=10, wis=10, cha=10,
    skills=["athletics", "intimidation", "perception", "survival", "animal_handling"],
    saving_throws=["str", "con"],
    ini=2, ac=17, max_hp=15, hit_dice="1d12", spd=25)

orikour.attacks = [
    "Battle Axe 1hd|+5|1d8+3", 
    "Battle Axe 2hd|+5|1d10+3",
    "Hand Axe|+5|1d6+3",
    "Hand Axe(R)|+4|1d6+3",
    "Javelin|+5|1d6+3",
    "Morningstar|+5|1d8+3",
    "Warhammer|+5|1d8+3",
]

orikour.proficiencies = [
    "Light & Medium Armor, Shields",
    "Martial & Light Weapons",
]



