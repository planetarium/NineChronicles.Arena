from sqlalchemy import Column, Integer, Enum, BigInteger, Index

from common.enums import ArenaType
from common.models.base import AutoIdMixin, Base


class Arena(AutoIdMixin, Base):
    __tablename__ = "arena"

    championship = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    arena_type = Column(Enum(ArenaType), nullable=False)
    start_block_index = Column(BigInteger, nullable=False)
    end_block_index = Column(BigInteger, nullable=False)

    __table_args__ = (
        Index("arena_championship_round_idx", "championship", "round"),
    )
