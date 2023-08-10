from dataclasses import dataclass
from typing import List, Union, Dict

from common.enums import ItemType, ItemSubType, ElementalType, StatType


@dataclass
class StatMapSchema:
    hP: int
    hIT: int
    aTK: int
    dEF: int
    cRI: int
    sPD: int

    @property
    def stats_map(self):
        return {
            StatType.HP: self.hP,
            StatType.HIT: self.hIT,
            StatType.ATK: self.aTK,
            StatType.DEF: self.dEF,
            StatType.CRI: self.cRI,
            StatType.SPD: self.sPD,
        }


@dataclass
class SkillSchema:
    id: int
    power: int
    chance: int
    statPowerRatio: int
    referencedStatType: StatType


@dataclass
class StatSchema:
    statType: StatType
    totalValue: int


@dataclass
class EquipmentSchema:
    id: int
    itemType: ItemType
    itemSubType: ItemSubType
    elementalType: ElementalType
    level: int
    itemId: str
    setId: int
    stat: Union[Dict, StatSchema]
    skills: Union[List[Dict], List[SkillSchema]]
    buffSkills: Union[List[Dict], List[SkillSchema]]
    statsMap: Union[Dict, StatMapSchema]

    def __post_init__(self):
        self.stat = StatSchema(**self.stat)
        self.skills = [SkillSchema(**sk) for sk in self.skills]
        self.buffSkills = [SkillSchema(**buff) for buff in self.buffSkills]
        self.statsMap = StatMapSchema(**self.statsMap)

    @property
    def stats_map(self):
        return self.statsMap.stats_map


@dataclass
class CostumeSchema:
    id: int
    itemType: ItemType
    itemSubType: ItemSubType
    itemId: str


@dataclass
class InventorySchema:
    equipments: Union[List[Dict], List[EquipmentSchema]]
    costumes: Union[List[Dict], List[CostumeSchema]]

    def __post_init__(self):
        self.equipments = [EquipmentSchema(**eq) for eq in self.equipments]
        self.costumes = [CostumeSchema(**cos) for cos in self.costumes]


@dataclass
class RuneSchema:
    runeId: int
    level: int


@dataclass
class AvatarStateSchema:
    address: str
    agentAddress: str
    name: str
    level: int
    characterId: int
    inventory: Union[Dict, InventorySchema]
    runes: Union[List[Dict], List[RuneSchema]]

    def __post_init__(self):
        self.inventory = InventorySchema(**self.inventory)
        self.runes = [RuneSchema(**x) for x in self.runes]
