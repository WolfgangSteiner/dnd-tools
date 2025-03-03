from math import ceil
import yaml

ABILITIES = ('str', 'dex', 'con', 'int', "wis", "cha")
STR_SKILLS = ('athletics', )
DEX_SKILLS = ('acrobatics', 'sleight_of_hand', 'open_locks', 'disarm_traps', 'stealth')
CON_SKILLS = tuple()
INT_SKILLS = ('arcana', 'history', 'investigation', 'nature', 'religion')
WIS_SKILLS = ('animal_handling', 'insight', 'medicine', 'perception', 'survival')
CHA_SKILLS = ('deception', 'intimidation', 'performance', 'persuation')
SKILLS_FOR_ABILITY = { 'str':STR_SKILLS, 'dex':DEX_SKILLS, 'con':CON_SKILLS,
                        'int':INT_SKILLS, 'wis':WIS_SKILLS, 'cha':CHA_SKILLS}

EXPLORERS_PACK = ['Bedroll', 'Mess Kit', 'Tinderbox', '10 Torches', '10 Rations', '50ft Rope', 'Waterskin']
DUNGEONEERS_PACK = ['Bedroll', 'Crowbar', 'Hammer', 'Pitons', 'Tinderbox', '10 Torches', '10 Rations', '50ft Rope', 'Waterskin']
ABILITY_FOR_SKILL = {skill:ability for ability,values in SKILLS_FOR_ABILITY.items() for skill in values}

def ability_for_skill(skill):
    return ABILITY_FOR_SKILL[skill.lower()]


def sort_skills(skills):
    skills = sorted(skills)
    sorted_skills = []
    for ability in ABILITIES:
        for skill in skills:
            if ability_for_skill(skill) == ability:
                sorted_skills.append(skill)
    return sorted_skills


class Character():
    def __init__(self, **kwargs):
        self.str = kwargs.get("str", 10)
        self.dex = kwargs.get("dex", 10)
        self.con = kwargs.get("con", 10)
        self.int = kwargs.get("int", 10)
        self.wis = kwargs.get("wis", 10)
        self.cha = kwargs.get("cha", 10)
        self.name = kwargs.get("name", "")
        self.level = kwargs.get("level", 1)
        self.xp = kwargs.get("xp", 0)
        self.ancestry = kwargs.get("ancestry", "Human")
        self.profession = kwargs.get("profession", "Commoner")
        self.skills = kwargs.get("skills", [])
        self.saving_throws = kwargs.get("saving_throws", [])
        self.ini = kwargs.get("ini", self.ability_modifier("dex"))
        self.ac = kwargs.get("ac", 10)
        self.max_hp = kwargs.get("max_hp", 10)
        self.hit_dice = kwargs.get("hit_dice", "1d6")
        self.spd = kwargs.get("spd", 30)
        self.attacks = kwargs.get("attacks", [f"Bare Hands|{self.ability_modifier('str'):+}"])
        self.proficiencies = kwargs.get("proficiencies", [])
        self.feats_traits = kwargs.get("feats_traits", [])
        self.gear =  kwargs.get("gear", [])
        self.backpack = kwargs.get("backpack", [])
        self.items = kwargs.get("items", [])
        self.passive_perception = kwargs.get("passive_perception", 10 + self.skill_modifier("perception"))
        self.is_spellcaster = kwargs.get("is_spellcaster", self.profession.lower() in ("wizard", "druid", "cleric"))
        self.notes = kwargs.get("notes", [])
        self.font = kwargs.get("font")
        self.gp = kwargs.get("gp", 0)
        self.sp = kwargs.get("sp", 0)
        self.personality = kwargs.get("personality", "")
        self.ideals = kwargs.get("ideals", "")
        self.bonds = kwargs.get("bonds", "")
        self.flaws = kwargs.get("flaws", "")


    @staticmethod
    def from_yaml(file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        abilities = data.get("abilities", {'str':10, 'dex':10, 'con':10, 'int':10, 'wis':10, 'cha':12})
        money= data.get("money", {'gp':0, 'sp':0})
        spd = data.get("speed", {'walk': 30})

        return Character(
            name=data.get("name", "Unknown"),
            ancestry=data.get("ancestry", "Unknown"),
            profession=data.get("profession", "None"),
            size=data.get("size", "medium"),
            level=data.get("level", 1),
            xp=data.get("xp", 0),
            str = abilities['str'],
            dex = abilities['dex'],
            con = abilities['con'],
            int = abilities['int'],
            wis = abilities['wis'],
            cha = abilities['cha'],
            skills = data.get("skills", []),
            saving_throws=data.get("saving_throws", []),
            ac=data.get("ac", 10),
            max_hp=data.get("max_hp", 1),
            hit_dice=data.get("hit_dice", "1d6"),
            spd=spd['walk'],
            gp=money['gp'],
            sp=money['sp'],
            attacks =data.get("attacks", []),
            proficiencies=data.get("proficiencies", []),
            feats_traits=data.get("feats_traits", []),
            gear=data.get("gear", []),
            backpack=data.get("backpack", []),
            items=data.get("items",[]),
            personality=data.get("personality", ""),
            ideals = data.get("ideals", ""),
            bonds = data.get("bonds", ""),
            flaws = data.get("flaws", ""),
            notes = data.get("notes", []),
        )

    @staticmethod
    def load_monsters_from_directory(directory):
        monsters = {}
        for file_name in glob.glob(f"{directory}/*.yml"):
            monster = Monster.from_yaml(file_name)
            monsters[monster.name.lower()] = monster
        return monsters



    def ability_modifier(self, ability):
        return int((getattr(self, ability) - 10) / 2)

    def skill_modifier(self, skill):
        ability = ability_for_skill(skill)
        mod = self.ability_modifier(ability)
        if skill in self.skills:
            mod += self.proficiency_bonus
        return mod

    def spell_slots_for_level(self, spell_lvl):
        if not self.is_spellcaster:
            return 0
        elif self.profession.lower() == "ranger":
            return self.spell_slots_for_level_ranger(spell_lvl)

        if spell_lvl == 1:
            return min(4, self.level + 1)
        elif spell_lvl == 2:
            return min(3, self.level - 1) if self.level >= 3 else 0
        elif spell_lvl == 3:
            return min(3, self.level - 3) if self.level >= 5 else 0
        elif spell_lvl == 4:
            return min(3, self.level - 6) if self.level >= 7 else 0
        elif spell_lvl == 5:
            if self.level >= 18:
                return 3
            elif self.level >= 9:
                return min(2, self.level - 8)
            else:
                return 0
        elif spell_lvl == 6:
            if self.level >= 19:
                return 2
            elif self.level >= 11:
                return 1
            else:
                return 0
        elif spell_lvl == 7:
            if self.level >= 20:
                return 2
            elif self.level >= 13:
                return 1
            else:
                return 0
        elif spell_lvl == 8:
            return 1 if self.level >= 15 else 0
        elif spell_lvl == 9:
            return 1 if self.level >= 17 else 0
        else:
            raise ValueError

    def spell_slots_for_level_ranger(self, spell_lvl):
        lvl = self.level
        if spell_lvl == 1:
            return 4 if lvl >= 5 else 3 if lvl >= 3 else 1 if lvl == 2 else 0
        else:
            return 0

    @property
    def spell_saving_dc(self):
        if not self.is_spellcaster:
            return 0
        elif self.profession.lower() in ("wizard",):
            return 8 + self.proficiency_bonus + self.ability_modifier("int")
        elif self.profession.lower() in ("druid", "cleric", "ranger"):
            return 8 + self.proficiency_bonus + self.ability_modifier("wis")


    @property
    def max_spell_level(self):
        if not self.is_spellcaster:
            return 0
        for lvl in range(9,0,-1):
            if self.spell_slots_for_level(lvl) > 0:
                return lvl
    

    @property
    def proficiency_bonus(self):
        return ceil(self.level / 4) + 1

