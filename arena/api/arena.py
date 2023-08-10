from typing import List, Tuple, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from arena.dependencies import session
from arena.schemas.arena import ArenaSchema
from arena.schemas.arena_info import ArenaParticipantSchema
from arena.schemas.avatar import FullAvatarSchema
from common.models.arena import Arena
from common.models.avatar import ArenaInfo, Equipment, Costume

router = APIRouter(
    prefix="/arena",
    tags=["Arena"],
)


def verify_arena(sess, championship: int, round: int) -> Tuple[bool, Optional[Arena]]:
    arena = sess.scalar(select(Arena).where(Arena.championship == championship, Arena.round == round))
    return arena is not None, arena


@router.get("", response_model=ArenaSchema)
def arena_info(block_index: int = None, championship: int = None, round: int = None, sess=Depends(session)):
    """
    # Arena Info

    Get basic arena information based on block index or championship/round.
    """
    if not (block_index or championship or round):
        raise ValueError("Either block_index or championship/round is required.")

    if block_index:
        err_msg = f"No arena found including block {block_index}."
        arena = sess.scalar(
            select(Arena).where(Arena.start_block_index <= block_index, Arena.end_block_index >= block_index))
    else:
        if not (championship and round):
            raise ValueError("Both championship and round are required.")

        err_msg = f"No arena of championship {championship} round {round} found."
        verified, arena = verify_arena(sess, championship, round)

        if not verified:
            raise ValueError(err_msg)

    return arena


@router.get("/participant-list", response_model=List[ArenaParticipantSchema])
def arena_participant_list(championship: int, round: int, avatar_addr: str, sess=Depends(session)):
    """
    # Arena participant list

    Get arena participant list around requested avatar.
    """
    verified, arena = verify_arena(sess, championship, round)
    if not verified:
        raise ValueError(f"No arena of championship {championship} round {round} found.")

    avatar_info = sess.scalar(
        select(ArenaInfo).where(ArenaInfo.arena_id == arena.id, ArenaInfo.avatar_addr == avatar_addr)
    )
    if not avatar_info:
        raise ValueError(f"No arena participant info for avatar {avatar_addr}")

    participant_list = (sess.query(ArenaInfo, func.rank().over(order_by=ArenaInfo.score.desc()).label("rank"))
                        .filter(ArenaInfo.score.between(avatar_info.score - 100, avatar_info.score + 200))
                        ).all()
    schema_list = []
    for pa in participant_list:
        schema = ArenaParticipantSchema.model_validate(pa.ArenaInfo)
        schema.rank = pa.rank
        schema_list.append(schema)
    return schema_list


@router.get("/avatar-info", response_model=FullAvatarSchema)
def full_avatar_info(championship: int, round: int, avatar_addr: str, sess=Depends(session)):
    """
    # Avatar Info

    Gets full avatar states info of given address.
    """
    verified, arena = verify_arena(sess, championship, round)
    if not verified:
        raise ValueError(f"No arena of championship {championship} round {round} found.")

    # FIXME: This query is very slow due to cartesian product of multiple tables.
    # avatar_info = sess.scalar(
    #     select(ArenaInfo).where(ArenaInfo.arena_id == arena.id, ArenaInfo.avatar_addr == avatar_addr)
    #     .options(joinedload(ArenaInfo.equipment_list).joinedload(Equipment.stats_list))
    #     .options(joinedload(ArenaInfo.equipment_list).joinedload(Equipment.all_skill_list))
    #     .where(Equipment.equipped.is_(True))
    #     .options(joinedload(ArenaInfo.costume_list))
    #     .where(Costume.equipped.is_(True))
    # )
    avatar_info = sess.scalar(
        select(ArenaInfo).where(ArenaInfo.arena_id == arena.id, ArenaInfo.avatar_addr == avatar_addr)
        .options(joinedload(ArenaInfo.costume_list.and_(Costume.equipped.is_(True))))
    )
    if not arena_info:
        raise ValueError(f"No arena participant info for avatar {avatar_addr}")

    equipment_list = sess.scalars(
        select(Equipment).where(Equipment.arena_info_id == avatar_info.id)
        .options(joinedload(Equipment.stats_list)).options(joinedload(Equipment.all_skill_list))
        .where(Equipment.equipped.is_(True))
    ).unique().fetchall()
    avatar_info.equipment_list = equipment_list

    return avatar_info
