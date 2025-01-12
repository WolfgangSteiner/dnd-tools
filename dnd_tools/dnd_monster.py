import os
import yaml
import glob

class Monster:
    def __init__(self, name, **kwargs):
        self.name = name
        self.type = kwargs.get("type")
        self.size = kwargs.get("size", "medium")
        self.ac = kwargs.get("ac", 10)
        self.hp = kwargs.get("hp", 1)
        self.hit_dice = kwargs.get("hit_dice", "1d6")
        self.speed = kwargs.get("speed", {"walk": 30})
        self.abilities = kwargs.get("abilities", {
            "str": 0, "dex": 0, "con": 0,
            "int": 0, "wis": 0, "cha": 0
        })
        self.saving_throws = kwargs.get("saving_throws", {})
        self.skills = kwargs.get("skills", {})
        self.specials = kwargs.get("specials", [])
        self.passive_perception = kwargs.get("passive_perception", 8)
        self.cr = kwargs.get("cr", 0)
        self.xp = kwargs.get("xp", 0)
        self.actions = kwargs.get("actions", [])
        self.bonus_actions = kwargs.get("bonus_actions", [])
        self.reactions = kwargs.get("reactions", [])
        self.immunities = kwargs.get("immunities", [])
        self.resistances = kwargs.get("resistances", [])
        self.gear = kwargs.get("gear", [])

    @property
    def as_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "ac": self.ac,
            "hp": self.hp,
            "hit_dice": self.hit_dice,
            "speed": self.speed,
            "abilities": self.abilities,
            "passive_perception": self.passive_perception,
            "saving_throws": self.saving_throws,
            "skills": self.skills,
            "specials": self.specials,
            "cr": self.cr,
            "xp": self.xp,
            "actions": self.actions,
            "bonus_actions": self.bonus_actions,
            "reactions": self.reactions,
            "resistances": self.resistances,
            "immunities": self.immunities,
        }

    @staticmethod
    def from_yaml(file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return Monster(
            name=data.get("name", "Unknown"),
            type=data.get("type", "Unknown"),
            ac=data.get("ac", 10),
            hp=data.get("hp", 1),
            hit_dice=data.get("hit_dice", "1d6"),
            speed=data.get("speed", [{"walk": 30}]),
            abilities=data.get("abilities", {
                "str": 0, "dex": 0, "con": 0,
                "int": 0, "wis": 0, "cha": 0
            }),
            saving_throws=data.get("saving_throws", {}),
            skills=data.get("skills", {}),
            cr=data.get("cr", 0),
            xp=data.get("xp", 0),
            specials=data.get("specials", []),
            actions=data.get("actions", []),
            bonus_actions=data.get("bonus_actions", []),
            reactions=data.get("reactions", []),
            resistances=data.get("resistances", []),
            immunities=data.get("immunities", []),
            size=data.get("size", "medium")
        )

    @staticmethod
    def load_monsters_from_directory(directory):
        monsters = {}
        for file_name in glob.glob(f"{directory}/*.yml"):
            monster = Monster.from_yaml(file_name)
            monsters[monster.name.lower()] = monster
        return monsters

# Usage Example
# monsters = load_monsters_from_directory("path_to_yaml_directory")
# print(monsters["Goblin"].as_dict)
