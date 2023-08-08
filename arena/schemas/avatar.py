from typing import Optional, List

from pydantic import BaseModel as BaseSchema

from common.enums import ItemType, ItemSubType, ElementalType, StatType


class EquipmentSkillSchema(BaseSchema):
    referenced_stat_type: StatType
    stat_power_ratio: int
    power: int
    chance: int

    class Config:
        from_attributes = True


class EquipmentStatSchema(BaseSchema):
    HP: Optional[int] = 0
    ATK: Optional[int] = 0
    DEF: Optional[int] = 0
    CRI: Optional[int] = 0
    HIT: Optional[int] = 0
    SPD: Optional[int] = 0
    DRV: Optional[int] = 0
    DRR: Optional[int] = 0
    CDMG: Optional[int] = 0
    APTN: Optional[int] = 0
    THORN: Optional[int] = 0

    class Config:
        from_attributes = True


class EquipmentSchema(BaseSchema):
    item_id: str
    sheet_id: int
    item_type: ItemType
    item_subtype: ItemSubType
    elemental_type: ElementalType
    level: int
    set_id: int
    stat_type: StatType
    stat_value: int
    equipped: bool

    stats_map: EquipmentStatSchema
    skill_list: List[EquipmentSkillSchema]
    buff_skill_list: List[EquipmentSkillSchema]

    class Config:
        from_attributes = True


class CostumeSchema(BaseSchema):
    sheet_id: int
    item_type: ItemType
    item_subtype: ItemSubType
    equipped: bool

    class Config:
        from_attributes = True


class InventorySchema(BaseSchema):
    equipment_list: List[EquipmentSchema]
    costume_list: List[CostumeSchema]


class FullAvatarSchema(BaseSchema):
    avatar_addr: str
    agent_addr: str
    name: str
    level: int
    character_id: int
    cp: int
    costume_armor_id: int
    title_id: Optional[int]
    inventory: InventorySchema

    class Config:
        from_attributes = True
