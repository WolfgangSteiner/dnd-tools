from dnd_tools.dnd_character import Character, EXPLORERS_PACK

melwen = Character(
    name="Melwen Moonarrow", ancestry="High Elf", profession="Ranger", is_spellcaster=True,
    level=2, xp=300,
    str=10, dex=16, con=14, int=10, wis=16, cha=8,
    skills=["animal_handling", "sleight_of_hand", "nature", "perception", "stealth"],
    saving_throws=["str", "dex"],
    ini=3, ac=18, max_hp=20, hit_dice="2d10", spd=30,
    font="TangerineBold")

melwen.background = "Urchin"
melwen.languages = "elvish, orkish, goblin, hafling"
melwen.attacks = [
    "Longbow|+7|1d8+3",
    "Rapier|+5|1d8+3",
    "Unarmed|+2|1",
]

melwen.proficiencies = [
    "Light & Medium Armor",
    "Shields",
    "Longsword, Shortsword",
    "Rapiers",
    "Shortbow, Longbow",
    "Quaterstaffs, Daggers",
    "Thief Tools",
]

melwen.feats_traits = [
    "Archery",
    "City Secrets",
    "Darkvision",
    "Favoured Enemy: Goblinoids",
    "Fey Ancestry",
    "Natural Explorer: Forest",
    "Trance",
]

melwen.gear = [
    "Scale Amour",
    "Long Bow",
    "Quiver",
    "Rapier",
    "Shield",
    "Waterskin",
]

melwen.backpack = ["Bedroll", "Mess Kit", "Tinderbox", "10 Torches", "10 Rations", "50ft Rope", "Thief Tools"]

melwen.items = [
    "Pet Mouse",
    "Token of my Parents",
]

melwen.notes = [ 
    "<b>Archery:</b> Gain +2 on ranged ATCK.",
    "<b>City Secrets:</b> Can travel twice as fast in city",
    "<b>Favoured Enemy:</b> ADV on WIS when tracking FE, ADV on INT recalling information about FE",
    "<b>Fey Ancestry:</b> ADV on SAV vs. Charm. Immune to sleep spells.",
    "<b>Natural Explorer</b>: PHB 91",
    "<b>Trance</b>: Meditation of 4hrs instead of sleep.",
]

melwen.personality = "I like to squeeze into small places where no one cat get me."
melwen.ideals = r"I am going to prove that I'm worthy of a better life."
melwen.bonds = "I sponsor an orphanage to keep others from enduring what I was forced to endure."
melwen.flaws = "I will never fully trust anyone other than myself."

