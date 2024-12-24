from dnd_tools import Character

tombur = Character(
    name="Tombur Rockseeker", level=2, ancestry="Mountain Dwarf", profession="Wizard",
    str=10, dex=12, con=16, int=18, wis=10, cha=12,
    skills=["acrobatics", "performance", "insight", "investigation"],
    saving_throws=["int", "wis"],
    ini=1, ac=17, max_hp=18, hit_dice="2d6", spd=25)

tombur.attacks = [
    "Quarterstaff|0|1d6"
]

tombur.proficiencies = [
    "Light & Medium Armor",
    "Quaterstaffs, Daggers",
    "Dwarven Combat Training",
    "Light Crossbows, Darts, Slings",
    "Disguise", "Lute", "Smithing"
]

tombur.feats_traits = [
    "By Popular Demand",
    "Dwarven Resilience",
    "Darkvision",
    "Arkane Recovery",
    "Evoker",
]



