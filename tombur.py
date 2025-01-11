from dnd_tools import Character

tombur = Character(
    name="Tombur Rockseeker", level=2, ancestry="Mountain Dwarf", profession="Wizard",
    str=10, dex=12, con=16, int=18, wis=10, cha=12,
    skills=["acrobatics", "performance", "insight", "investigation"],
    saving_throws=["int", "wis"],
    ini=1, ac=17, max_hp=18, hit_dice="2d6", spd=25)

tombur.attacks = [
    "Quarterstaff|+2|1d6",
    "Fire Bolt|+6|1d10",
    "Ray of Frost|+6|1d8",
]

tombur.proficiencies = [
    "Light & Medium Armor",
    "Quaterstaffs, Daggers",
    "Dwarven Combat Training",
    "Light Crossbows",
    "Darts, Slings",
    "Disguise", "Lute", "Smithing"
]

tombur.feats_traits = [
    "By Popular Demand",
    "Dwarven Resilience",
    "Darkvision",
    "Arkane Recovery",
    "Evoker",
]

tombur.personality = "I can defuse any tension in the room."
tombur.ideals = r"I like seeing the smiles on people's faces when I perform."
tombur.bonds = "My instrument is my most treasured possession."
tombur.flaws = "My sharp toungue keeps getting me in trouble with the people in power."
