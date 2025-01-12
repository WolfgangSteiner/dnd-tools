from dnd_tools import Character

orikour = Character(
    name="Orikour Whiteforge", ancestry="Mountain Dwarf", profession="Barbarian",
    level=2, xp=300,
    str=16, dex=14, con=16, int=10, wis=10, cha=10,
    skills=["athletics", "intimidation", "perception", "survival", "animal_handling"],
    saving_throws=["str", "con"],
    ini=2, ac=17, max_hp=29, hit_dice="2d12", spd=25)

orikour.attacks = [
    "Battle Axe 1hd|+5|1d8+3", 
    "Battle Axe 2hd|+5|1d10+3",
    "Javelin|+5|1d6+3",
    "Warhammer|+5|1d8+3",
]

orikour.proficiencies = [
    "Light & Medium Armor",
    "Shields",
    "Martial & Light Weapons",
    "Battleaxes, Hand Axes",
    "Warhammers",
]

orikour.feats_traits = [
    "Dwarven Resilience",
    "Dwarven Combat Training",
    "Darkvision",
    "Danger Sense",
    "Rage (2 per Long Rest)",
    "Reckless Attack",
    "Unarmored Defence",
]
orikour.gear = [
    "Battle Axe",
    "Warhammer",
    "Shield",
    "4x Javelin",
    "Traveller's Clothes",
    "Waterskin",
]

orikour.backpack = [
    "Bedroll", "Mess Kit", "10 Torches", "Tinderbox", "10 Rations", "50ft Rope"
]

orikour.personality = "I like to break things! A simple, direct solution is the best."
orikour.ideals = "My people are all that matter."
orikour.bonds = "I would lay my life down for my comrades."
orikour.flaws = "My hatred of my enemies is blind and unreasoning."
orikour.notes = [
    "<b>Danger Sense</b>: ADV on DEX.SAV against effects you can see (traps, spells).",
    "<b>Dwarven Resilience</b>: Resitance against Poison, Adv on poison SAV.",
    "<b>Rage</b>: Adv on STR checks and saving throws, +2 melee dmg, res. to blunt, piercing, slashing damage.",
    "<b>Reckless Attack</b>: Gain ADV on 1st attack, but foes also gain ADV on attacks until next turn.",
    "<b>Unarmored Defence</b>: Add CON.MOD to AC when not wearing armor.",
]

