import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Dict

import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from common.models.avatar import ArenaInfo
from common.schemas.action import JoinArena3Schema
from common.schemas.block import BlockSchema
from tests.monkeypatch.arena_updater import mock_get_avatar_state
from worker.worker.arena_updater import join_arena, decode_item_id

TEST_JOIN_ARENA_DATA = {
    "id": "0xe5d183536215c34e929d963f060f0f1c",
    "championshipId": 1,
    "round": 1,
    "avatarAddress": "0x211939355049999363383840912",
    "costumes": ["0xd4666c069fc43e4e8fa278d85f6cdcab", "0x1572a5bb6fee7846a0fb0a2a76e5589c"],
    "equipments": ["0x15d813109c0fd54d92af20b43d0c273c", "0xbf84531d3d86ce449eaa5b88dd9d5f3e",
                   "0xac40187a48ff5d4d9c9450664d80f534", "0x2e7a699a5c6a1643b59b717725d6e15c"],
    "runeInfos": [["0", "10011"], ["1", "10012"], ["3", "10003"], ["4", "10013"]]
}


def generate_block(data: Dict) -> BlockSchema:
    return BlockSchema(**{
        "index": 1,
        "hash": "123",
        "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        "transactions": [{"actions": [
            {"json": json.dumps({"type_id": "join_arena3", "values": data})}
        ]}, ]
    })


@pytest.mark.usefixtures("session", "setup")
def test_adding_new_join_arena(session, monkeypatch):
    monkeypatch.setattr("worker.worker.arena_updater.get_avatar_state", mock_get_avatar_state)
    test_data = JoinArena3Schema(**TEST_JOIN_ARENA_DATA)
    test_block = generate_block(TEST_JOIN_ARENA_DATA)
    join_arena(session, test_block)

    expected_equipped = {decode_item_id(x) for x in (test_data.equipments + test_data.costumes)}

    data = session.scalar(select(ArenaInfo)
                          .options(joinedload(ArenaInfo.arena))
                          .options(joinedload(ArenaInfo.equipment_list))
                          .options(joinedload(ArenaInfo.costume_list))
                          )
    assert data.avatar_addr == test_data.avatarAddress
    assert data.arena.championship == test_data.championshipId
    assert data.arena.round == test_data.round

    for eq in data.equipment_list:
        if eq.equipped:
            assert eq.id in expected_equipped
            expected_equipped.remove(eq.id)
    for cos in data.costume_list:
        if cos.equipped:
            assert cos.id in expected_equipped
            expected_equipped.remove(cos.id)
    assert len(expected_equipped) == 0


@pytest.mark.usefixtures("session", "setup")
def test_adding_existing_avatar(session, monkeypatch):
    monkeypatch.setattr("worker.worker.arena_updater.get_avatar_state", mock_get_avatar_state)
    test_block = generate_block(TEST_JOIN_ARENA_DATA)
    join_arena(session, test_block)
    # This must be ignored
    join_arena(session, test_block)

    count = session.scalar(select(func.count(ArenaInfo.id)))
    assert count == 1


@pytest.mark.usefixtures("session", "setup")
def test_adding_wrong_arena(session, monkeypatch):
    prev_count = session.scalar(select(func.count(ArenaInfo.id)))
    monkeypatch.setattr("worker.worker.arena_updater.get_avatar_state", mock_get_avatar_state)
    test_arena_data = deepcopy(TEST_JOIN_ARENA_DATA)
    test_arena_data["round"] = 99
    test_block = generate_block(test_arena_data)
    join_arena(session, test_block)

    count = session.scalar(select(func.count(ArenaInfo.id)))
    assert count == prev_count

    # with pytest.raises(ValueError) as e:
    #     join_arena(session, test_block)
    #     assert str(e) == f"There is no Arena of Championship {test_data.championshipId} Round {test_data.round}"
