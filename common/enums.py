from enum import Enum


class ArenaType(Enum):
    OffSeason = "OffSeason"
    Season = "Season"
    Championship = "Championship"


class ItemType(Enum):
    CONSUMABLE = 0
    COSTUME = 1
    EQUIPMENT = 2
    MATERIAL = 3


class ItemSubType(Enum):
    # Consumable
    FOOD = 0

    # Costume
    FULL_COSTUME = 1
    HAIR_COSTUME = 2
    EAR_COSTUME = 3
    EYE_COSTUME = 4
    TAIL_COSTUME = 5

    # Equipment
    WEAPON = 6
    ARMOR = 7
    BELT = 8
    NECKLACE = 9
    RING = 10

    # Material
    EQUIPMENT_MATERIAL = 11
    FOOD_MATERIAL = 12
    MONSTER_PART = 13
    NORMAL_MATERIAL = 14
    HOURGLASS = 15
    AP_STONE = 16
    ## Obsoleted
    CHEST = 17

    # Costume
    TITLE = 18


class ElementalType(Enum):
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    LAND = "Land"
    WIND = "Wind"


class StatType(Enum):
    # See `STatType.cs` in Lib9c
    NONE = "NONE"
    HP = "HP"
    ATK = "Attack"
    DEF = "Defence"
    CRI = "Critical"
    HIT = "Hit"
    SPD = "Speed"
    DRV = "Damage Reduction Value"
    DRR = "Damage Reduction Rate"
    CDMG = "Critical Damage"
    APTN = "ArmorPenetration"
    THORN = "Thorn"


class SkillType(Enum):
    SKILL = "Skill"
    BUFF_SKILL = "BuffSkill"
