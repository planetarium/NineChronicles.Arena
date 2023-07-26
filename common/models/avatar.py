from sqlalchemy import Text, Column, ForeignKey, Integer
from sqlalchemy.orm import backref, relationship

from common.const import ARENA_START_SCORE
from common.models.base import Base, AutoIdMixin


class Avatar(Base):
    __tablename__ = "avatar"

    addr = Column(Text, primary_key=True, nullable=False, index=True)
    agent_addr = Column(Text)
    level = Column(Integer, nullable=False)
    costume_armor_id = Column(Integer, nullable=False, default=10200000,
                              doc="Full costume or armor ID to draw profile image")
    title_id = Column(Integer, nullable=True)
    # cp = Column(Integer)


class ArenaInfo(AutoIdMixin, Base):
    __tablename__ = "arena_info"

    avatar_addr = Column(Text, ForeignKey("avatar.addr"), nullable=False)
    avatar = relationship("Avatar", foreign_keys=[avatar_addr], backref=backref("arena_info", uselist=False))
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

    # __table_args__ = (
    #     Index("avatar_arena_id_idx", "avatar_addr", "championship", "round"),
    # )
