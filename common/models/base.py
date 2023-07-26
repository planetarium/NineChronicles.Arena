from sqlalchemy import Column, Integer, func, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AutoIdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)


class TimestampMixin:
    # https://spoqa.github.io/2019/02/15/python-timezone.html
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
