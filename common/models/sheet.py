from decimal import *

from sqlalchemy import Column, Integer, Text, Enum, Index, Float

from common.enums import StatType
from common.models.base import Base, AutoIdMixin


class CharacterSheet(Base):
    __tablename__ = "character_sheet"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)  # _name in CSV file
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    dfc = Column(Integer, nullable=False)  # defence. def in CSV file
    cri = Column(Integer, nullable=False)
    hit = Column(Integer, nullable=False)
    spd = Column(Integer, nullable=False)
    lv_hp = Column(Float, nullable=False)
    lv_atk = Column(Float, nullable=False)
    lv_dfc = Column(Float, nullable=False)  # defence. lv_def in CSV file
    lv_cri = Column(Float, nullable=False)
    lv_hit = Column(Float, nullable=False)
    lv_spd = Column(Float, nullable=False)


class EquipmentItemSheet(Base):
    __tablename__ = "equipment_item_sheet"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)  # _name in CSV file
    type = Column(Enum(StatType), nullable=False)  # stat_type in CSV file
    value = Column(Integer, nullable=False)  # stat_value in CSV file


class CostumeStatSheet(Base):
    __tablename__ = "costume_stat_sheet"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(StatType), nullable=False)  # stat_type in CSV file
    value = Column(Integer, nullable=False)  # stat_value in CSV file


class RuneOptionSheet(AutoIdMixin, Base):
    __tablename__ = "rune_option_sheet"

    rune_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)  # _name in CSV file
    level = Column(Integer, nullable=False)
    cp = Column(Integer, nullable=False)

    __table_args__ = (
        Index("rune_id_name_idx", "rune_id", "level"),
    )

    def get_cp(self, level: int) -> Decimal:
        return Decimal(self.cp)
