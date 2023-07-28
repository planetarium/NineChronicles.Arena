from sqlalchemy import Text, Column, ForeignKey, Integer, Index
from sqlalchemy.orm import backref, relationship

from common.const import ARENA_START_SCORE
from common.models.base import Base, AutoIdMixin


class ArenaInfo(AutoIdMixin, Base):
    # Create new arena info for same avatar every season
    __tablename__ = "arena_info"

    avatar_addr = Column(Text, nullable=False)
    agent_addr = Column(Text)
    level = Column(Integer, nullable=False)
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
