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
    equipped: bool
    stat: Union[Dict, StatSchema]
    skills: Union[List[Dict], List[SkillSchema]]
    buffSkills: Union[List[Dict], List[SkillSchema]]
    statsMap: StatMapSchema

    def __post_init__(self):
        self.stat = StatSchema(**self.stat)
        self.skills = [SkillSchema(**sk) for sk in self.skills]
        self.buffSkills = [SkillSchema(**buff) for buff in self.buffSkills]


@dataclass
class CostumeSchema:
    id: int
    itemType: ItemType
    itemSubType: ItemSubType
    itemId: str
    equipped: bool


@dataclass
class InventorySchema:
    equipments: Union[List[Dict], List[EquipmentSchema]]
    costumes: Union[List[Dict], List[CostumeSchema]]

    def __post_init__(self):
        self.equipments = [EquipmentSchema(**eq) for eq in self.equipments]
        self.costumes = [CostumeSchema(**cos) for cos in self.costumes]


@dataclass
class AvatarStateSchema:
    address: str
    agentAddress: str
    name: str
    level: int
    inventory: Union[Dict, InventorySchema]

    def __post_init__(self):
        self.inventory = InventorySchema(**self.inventory)
