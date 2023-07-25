import random
import secrets
from typing import List

from fastapi import APIRouter

from arena.schemas.arena_info import ArenaInfoSchema, ArenaBoardDataSchema
from common.const import ARENA_START_SCORE

router = APIRouter(
    prefix="/dummy-arena",
    tags=["Dummy"],
)


@router.get("/my", response_model=ArenaInfoSchema)
def arena_info(championship: int, arena_round: int, avatar_addr: str):
    """
    # Dummy Arena Info

    This API returns dummy arena info of requested avatar.
    All personal data are random and will be changed every request.
    """
    return ArenaInfoSchema(
        championship=championship,
        round=arena_round,
        addr=avatar_addr,
        win=random.choice(range(11)),
        lose=random.choice(range(11)),
        ticket=random.choice(range(9)),
        ticket_reset_count=random.choice(range(3)),
        purchased_ticket_count=random.choice(range(9))
    )


@router.get("/board", response_model=List[ArenaBoardDataSchema])
def arena_board_data(championship: int, arena_round: int, avatar_addr: str):
    """
    # Dummy Arena Board Data

    This API returns dummy arena board info.
    All data are random.
    """
    cnt = random.choice(range(10, 100))
    board_data = []
    my_index = random.choice(range(cnt))
    for i in range(cnt):
        board_data.append(ArenaBoardDataSchema(
            addr=avatar_addr if i == my_index else f"0x{secrets.token_hex(20)}",
            name=f"dummy_{i}",
            level=random.choice(range(300)),
            costume_id=10200000,
            score=ARENA_START_SCORE if i == my_index else random.choice(range(900, 1200)),
        ))
    board_data.sort(key=lambda x: x.score, reverse=True)
    for i, data in enumerate(board_data):
        data.rank = i + 1
        data.expect_win_score = 20 if data.score > ARENA_START_SCORE else 18

    return board_data
