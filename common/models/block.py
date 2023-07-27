from sqlalchemy import Column, Integer, Text, DateTime

from common.models.base import Base


class Block(Base):
    __tablename__ = "block"

    index = Column(Integer, index=True, primary_key=True)
    hash = Column(Text)
    timestamp = Column(DateTime)
