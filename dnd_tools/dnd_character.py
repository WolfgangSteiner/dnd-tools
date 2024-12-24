from math import ceil

ABILITIES = ('str', 'dex', 'con', 'int', "wis", "cha")
STR_SKILLS = ('athletics', )
DEX_SKILLS = ('acrobatics', 'sleight_of_hand', 'stealth')
CON_SKILLS = tuple()
INT_SKILLS = ('arcana', 'history', 'investigation', 'nature', 'religion')
WIS_SKILLS = ('animal_handling', 'insight', 'medicine', 'perception', 'survival')
CHA_SKILLS = ('deception', 'intimidation', 'performance', 'persuation')
SKILLS_FOR_ABILITY = { 'str':STR_SKILLS, 'dex':DEX_SKILLS, 'con':CON_SKILLS,
                        'int':INT_SKILLS, 'wis':WIS_SKILLS, 'cha':CHA_SKILLS}

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
        self.proficiencies = []
        self.feats_traits = []
        self.gear = []
        self.items = []
        self.passive_perception = kwargs.get("passive_perception", 10 + self.skill_modifier("perception"))
        self.is_spellcaster = kwargs_get("is_spellcaster", self.profession in ("wizard", "druid"))

    def ability_modifier(self, ability):
        return int((getattr(self, ability) - 10) / 2)

    def skill_modifier(self, skill):
        ability = ability_for_skill(skill)
        mod = self.ability_modifier(ability)
        if skill in self.skills:
            mod += self.proficiency_bonus
        return mod

    @property
    def proficiency_bonus(self):
        return ceil(self.level / 4) + 1


