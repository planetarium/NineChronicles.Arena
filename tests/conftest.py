import os

import alembic.command
import pytest
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, scoped_session

from common.enums import ArenaType
from common.models.arena import Arena
from common.models.avatar import ArenaInfo, Costume, Skill, Equipment, EquipmentStat
from common.models.sheet import CharacterSheet

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
    char_sheet_data = [
        {"id": 100010, "name": "전사",
         "hp": 300, "atk": 20, "dfc": 10, "cri": 10, "hit": 90, "spd": 70,
         "lv_hp": 12, "lv_atk": 0.8, "lv_dfc": 0.4, "lv_cri": 0, "lv_hit": 3.6, "lv_spd": 2.8}
    ]
    try:
        for data in arena_data:
            session.add(Arena(**data))
        for data in char_sheet_data:
            session.add(CharacterSheet(**data))
        session.commit()
        yield
    finally:
        session.execute(delete(EquipmentStat))
        session.execute(delete(Costume))
        session.execute(delete(Skill))
        session.execute(delete(Equipment))
        session.execute(delete(ArenaInfo))

        session.execute(delete(CharacterSheet))
        session.execute(delete(Arena))

        session.commit()
