import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from common.models.avatar import ArenaInfo
from common.schemas.action import JoinArena3Schema
from tests.monkeypatch.arena_updater import mock_get_avatar_state
from worker.arena_updater import join_arena, decode_item_id

TEST_JOIN_ARENA_DATA = {
    "id": "0xe5d183536215c34e929d963f060f0f1c",
    "championshipId": 1,
    "round": 1,
    "avatarAddress": "0xDD21DCc1A9d393550A49999363e383c8409Ee1A2",
    "costumes": ["0xd4666c069fc43e4e8fa278d85f6cdcab", "0x1572a5bb6fee7846a0fb0a2a76e5589c"],
    "equipments": ["0x15d813109c0fd54d92af20b43d0c273c", "0xbf84531d3d86ce449eaa5b88dd9d5f3e",
                   "0xac40187a48ff5d4d9c9450664d80f534", "0x2e7a699a5c6a1643b59b717725d6e15c"],
    "runeInfos": [["0", "10011"], ["1", "10012"], ["3", "10003"], ["4", "10013"]]

}


@pytest.mark.usefixtures("session", "setup")
def test_adding_new_join_arena(session, monkeypatch):
    monkeypatch.setattr("worker.arena_updater.get_avatar_state", mock_get_avatar_state)
    test_data = JoinArena3Schema(**TEST_JOIN_ARENA_DATA)
    join_arena(session, test_data)

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
    monkeypatch.setattr("worker.arena_updater.get_avatar_state", mock_get_avatar_state)
    test_data = JoinArena3Schema(**TEST_JOIN_ARENA_DATA)
    join_arena(session, test_data)
    # This must be ignored
    join_arena(session, test_data)

    count = session.scalar(select(func.count(ArenaInfo.id)))
    assert count == 1


@pytest.mark.usefixtures("session", "setup")
def test_adding_wrong_arena(session, monkeypatch):
    monkeypatch.setattr("worker.arena_updater.get_avatar_state", mock_get_avatar_state)
    test_data = JoinArena3Schema(**TEST_JOIN_ARENA_DATA)
    test_data.round = 99
    with pytest.raises(ValueError) as e:
        join_arena(session, test_data)
        assert str(e) == f"There is no Arena of Championship {test_data.championshipId} Round {test_data.round}"
