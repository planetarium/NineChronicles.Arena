from sqlalchemy import Text, Column, ForeignKey, Integer, Index, Enum, Boolean
from sqlalchemy.orm import backref, relationship

from common.const import ARENA_START_SCORE
from common.enums import StatType, ItemSubType, ItemType, ElementalType, SkillType
from common.models.base import Base, AutoIdMixin


class ArenaInfo(AutoIdMixin, Base):
    # Create new arena info for same avatar every season
    __tablename__ = "arena_info"

    avatar_addr = Column(Text, nullable=False)
    agent_addr = Column(Text)
    level = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    cp = Column(Integer, nullable=False, default=0, doc="Total CP of this avatar.")
    costume_armor_id = Column(Integer, nullable=False, default=10200000,
                              doc="Full costume or armor ID to draw profile image")
    title_id = Column(Integer, nullable=True)
    arena_id = Column(Integer, ForeignKey("arena.id"), nullable=False)
    arena = relationship("Arena", foreign_keys=[arena_id], backref=backref("participant_list"))
    # championship = Column(Integer, nullable=False)
    # round = Column(Integer, nullable=False)
    win = Column(Integer, nullable=False, default=0)
    lose = Column(Integer, nullable=False, default=0)
    ticket = Column(Integer, nullable=False, default=0)
    ticket_reset_count = Column(Integer, nullable=False, default=0)
    purchased_ticket_count = Column(Integer, nullable=False, default=0)
    score = Column(Integer, nullable=False, default=ARENA_START_SCORE)
    # ranking = Column(Integer, nullable=False)

    __table_args__ = (
        Index("avatar_arena_id_idx", "avatar_addr", "arena_id"),
    )


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Text, primary_key=True, doc="Unique ID of item. (`itemId` in GQL query result)")
    arena_info_id = Column(Integer, ForeignKey("arena_info.id"), nullable=False)
    arena_info = relationship("ArenaInfo", foreign_keys=[arena_info_id], backref=backref("equipment_list"))
    # avatar_addr = Column(Text, ForeignKey("arena_info.avatar_addr"), nullable=False)
    # avatar = relationship("Avatar", foreign_keys=[avatar_addr], backref=backref("equipment_list"))
    sheet_id = Column(Integer, nullable=False, doc="Item id in CSV like 10541000. (`id` in GQL query result)")
    item_type = Column(Enum(ItemType))
    item_subtype = Column(Enum(ItemSubType))
    elemental_type = Column(Enum(ElementalType))
    level = Column(Integer)
    set_id = Column(Integer)
    stat_type = Column(Enum(StatType))
    stat_value = Column(Integer, doc="stat.totalValue in item state")
    equipped = Column(Boolean, default=False)


class EquipmentStat(AutoIdMixin, Base):
    __tablename__ = "equipment_stat"
    equipment_id = Column(Text, ForeignKey("equipment.id"), nullable=False)
    equipment = relationship("Equipment", foreign_keys=[equipment_id], backref=backref("stats_list"))
    stat_type = Column(Enum(StatType), nullable=False)
    stat_value = Column(Integer, nullable=False)


class Skill(AutoIdMixin, Base):
    __tablename__ = "skill"
    type = Column(Enum(SkillType), nullable=False)
    equipment_id = Column(Text, ForeignKey("equipment.id"), nullable=False)
    equipment = relationship("Equipment", foreign_keys=[equipment_id], backref=backref("all_skill_list"))
    skill_id = Column(Integer, nullable=False)
    referenced_stat_type = Column(Enum(StatType))
    stat_power_ratio = Column(Integer)
    power = Column(Integer)
    chance = Column(Integer)


class Costume(Base):
    __tablename__ = "costume"
    id = Column(Text, primary_key=True, doc="Unique ID of costume. (`itemId` in GQL query result)")
    # avatar_addr = Column(Text, ForeignKey("arena_info.avatar_addr"), nullable=False)
    # avatar = relationship("Avatar", foreign_keys=[avatar_addr], backref=backref("costume_list"))
    arena_info_id = Column(Integer, ForeignKey("arena_info.id"), nullable=False)
    arena_info = relationship("ArenaInfo", foreign_keys=[arena_info_id], backref=backref("costume_list"))
    sheet_id = Column(Integer, nullable=False, doc="Item id in CSV like 40100000. (`id` in GQL query result)")
    item_type = Column(Enum(ItemType))
    item_subtype = Column(Enum(ItemSubType))
    equipped = Column(Boolean, default=False)
