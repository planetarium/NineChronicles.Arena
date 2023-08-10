from pydantic import BaseModel as BaseSchema

from common.enums import ArenaType


class ArenaSchema(BaseSchema):
    arena_type: ArenaType
    championship: int
    round: int
    start_block_index: int
    end_block_index: int

    class Config:
        from_attributes = True
