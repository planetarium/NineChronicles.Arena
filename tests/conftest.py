import os

import alembic.command
import pytest
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, scoped_session

from common.enums import ArenaType
from common.models.arena import Arena
from common.models.avatar import ArenaInfo, Costume, Skill, Equipment

if os.path.exists(".env.test"):
    load_dotenv(".env.test")
else:
    # Gonna use os.environ
    pass


@pytest.fixture(scope="session")
def session():
    alembic.command.upgrade(Config("tests/alembic.ini", ini_section="test"), "head")
    engine = create_engine(os.environ.get("DB_URI"), echo=os.environ.get("DB_ECHO") in ("True", "true"))
    sess = scoped_session(sessionmaker(engine))
    try:
        yield sess
    finally:
        sess.rollback()
        sess.close()


@pytest.mark.usefixtures("session")
@pytest.fixture(scope="session")
def setup(session):
    arena_data = [
        {"championship": 1, "round": 1, "arena_type": ArenaType.OffSeason,
         "start_block_index": 1, "end_block_index": 100},
        {"championship": 1, "round": 2, "arena_type": ArenaType.Season,
         "start_block_index": 101, "end_block_index": 200},
        {"championship": 1, "round": 3, "arena_type": ArenaType.OffSeason,
         "start_block_index": 201, "end_block_index": 300},
        {"championship": 1, "round": 4, "arena_type": ArenaType.Championship,
         "start_block_index": 301, "end_block_index": 400},
    ]
    try:
        for data in arena_data:
            session.add(Arena(**data))
        session.commit()
        yield
    finally:
        session.execute(delete(Costume))
        session.execute(delete(Skill))
        session.execute(delete(Equipment))
        session.execute(delete(ArenaInfo))
        session.commit()
