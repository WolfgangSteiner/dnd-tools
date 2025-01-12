from dnd_tools import Character

gaia = Character(
    name="Gaia Galanodel", ancestry="High Elf", profession="Cleric",
    level=2, xp=300,
    str=14, dex=16, con=14, int=10, wis=17, cha=10,
    skills=["arcana", "history", "medicine", "insight", "perception"],
    saving_throws=["wis", "cha"],
    ini=3, ac=18, max_hp=17, hit_dice="2d8", spd=30,
    font="TangerineBold")

gaia.background = "Sage"
gaia.languages = "elvish, orkish, goblin, hafling"
gaia.attacks = [
    "Mace|+4|1d6+2",
    "Light Crossbow|+5|1d8+3",
]

gaia.proficiencies = [
    "Light & Medium Armor",
    "Heavy Armor",
    "Shields",
    "Longsword, Shortsword",
    "Shortbow, Longbow",
    "Quaterstaffs, Daggers",
    "Light Crossbows",
    "Darts, Slings",
]

gaia.feats_traits = [
    "Channel Divinity",
    "Darkvision",
    "Disciple of Life",
    "Fey Ancestry",
    "Researcher",
    "Trance",
]

gaia.gear = [
    "Scale Amour",
    "Mace",
    "Shield",
    "Light Crossbow",
    "Holy Symbol",
    "Waterskin",
    "Traveller's Clothes",
]

gaia.backpack = [
    "Bedroll",
    "Mess Kit",
    "Tinderbox",
    "10 Torches",
    "10 Rations",
    "50ft Rope",
]

gaia.items = [
    "Ink & Quill",
    "Knife",
    "Letter from Dead Colleague",
]


gaia.notes = [ 
    "<b>Channel Divinity:</b> Once per SR or LR <i>Turn Undead</i> or <i>Preserve Life</i>",
    "<b>Disciple of Life</b> Healing spells gain additional (2 + spell level) HP.",
    "<b>Fey Ancestry:</b> Advantage on saving throws against charm. Immune to sleep spells.",
    "<b>Preserve Life</b> Heal all creatures within 30ft by a total of (5 * level) HP.",
    "<b>Researcher</b>: Know where to obtain unknown information.",
    "<b>Trance</b>: Meditation of 4hrs per day may replace a night of sleep.",
]

gaia.personality = "I have read every book in the world's greates libraries."
gaia.ideals = r"The goal of a life of study is the betterment of oneself. "
gaia.bonds = "I have an ancient text that holds terrible secrets that must not fall into the wrong hands."
gaia.flaws = "I speak without really thinking through my words, invariably insulting others."

