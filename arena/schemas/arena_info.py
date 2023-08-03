from typing import Optional

from pydantic import BaseModel as BaseSchema


class ArenaInfoSchema(BaseSchema):
    championship: int
    round: int
    addr: str
    win: int
    lose: int
    ticket: int
    ticket_reset_count: int
    purchased_ticket_count: int



class ArenaParticipantSchema(BaseSchema):
    avatar_addr: str
    # name: str
    level: int
    costume_id: int = 10200000
    title_id: Optional[int] = None
    score: int
    rank: int = 0
    expect_win_score: int = 0
