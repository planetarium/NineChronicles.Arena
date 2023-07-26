from enum import Enum


class ArenaType(Enum):
    OffSeason = "OffSeason"
    Season = "Season"
    Championship = "Championship"


class StatType(Enum):
    # See `STatType.cs` in Lib9c
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
