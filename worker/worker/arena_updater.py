import os
import random
from time import time
from typing import List
from uuid import UUID

from sqlalchemy import select

from common import logger
from common.const import HOST_DICT
from common.enums import SkillType, ItemSubType
from common.models.arena import Arena
from common.models.avatar import ArenaInfo, Costume, Equipment, Skill, EquipmentStat
from common.schemas.action import JoinArena3Schema, BattleArena12Schema
from common.schemas.avatar import AvatarStateSchema
from common.schemas.block import BlockSchema
from common.utils.gql import execute_gql

from common.utils.cp import CPCalculator

stage = os.environ.get("STAGE", "development")
HOST = random.choice(HOST_DICT[stage])


def decode_item_id(encoded: str) -> str:
    bs = bytes.fromhex(encoded[2:])
    return str(UUID(bytes_le=bs))


def get_avatar_state(avatar_addr: str) -> AvatarStateSchema:
    query = f"""{{
    stateQuery {{
        avatar (
            avatarAddress: "{avatar_addr}"
        ) {{
            address agentAddress name level characterId
            inventory {{
                equipments {{
                    id itemType itemSubType elementalType level itemId setId equipped
                    stat {{
                        statType totalValue
                    }}
                    skills {{
                        id referencedStatType statPowerRatio power chance
                    }}
                    buffSkills {{
                        id referencedStatType statPowerRatio power chance
                    }}
                    statsMap {{
                        hP hIT aTK dEF cRI sPD
                    }}
                }}
                costumes {{
                    id itemType itemSubType itemId equipped
                }}
            }}
        }}
    }}
    }}
    """
    resp = execute_gql(f"{HOST}/graphql", query)
    return AvatarStateSchema(**resp["stateQuery"]["avatar"])


def join_arena(sess, data: JoinArena3Schema):
    # join_arena3
    # TODO: Create new avatar for new challenger
    target_arena = sess.scalar(
        select(Arena).where(Arena.championship == data.championshipId, Arena.round == data.round)
    )
    if not target_arena:
        msg = f"There is no Arena of Championship {data.championshipId} Round {data.round}"
        logger.error(msg)
        raise ValueError(msg)

    prev_info = sess.scalar(
        select(ArenaInfo.id).where(ArenaInfo.arena_id == target_arena.id,
                                   ArenaInfo.avatar_addr == data.avatarAddress)
    )
    if prev_info:
        logger.warning(
            f"Avatar {data.avatarAddress} has already been joined to arena {data.championshipId}:{data.round}")
        return

    avatar_state_schema = get_avatar_state(data.avatarAddress)
    equipped_items = {decode_item_id(x) for x in (data.equipments + data.costumes)}

    arena_info = ArenaInfo(
        avatar_addr=data.avatarAddress,
        arena_id=target_arena.id,
        agent_addr=avatar_state_schema.agentAddress,
        name=avatar_state_schema.name,
        level=avatar_state_schema.level,
        character_id=avatar_state_schema.characterId,
    )

    equipment_list = []
    costume_list = []

    for eq in avatar_state_schema.inventory.equipments:
        equipment = Equipment(
            arena_info=arena_info,
            id=eq.itemId,
            sheet_id=eq.id,
            item_type=eq.itemType,
            item_subtype=eq.itemSubType,
            level=eq.level,
            set_id=eq.setId,
            stat_type=eq.stat.statType,
            stat_value=eq.stat.totalValue,
            equipped=eq.itemId in equipped_items
        )

        stats_list = []
        for stat_type, stat_value in eq.stats_map.items():
            if stat_value != 0:
                stats_list.append(EquipmentStat(
                    equipment=equipment,
                    stat_type=stat_type,
                    stat_value=stat_value
                ))
        equipment.stats_list = stats_list

        skill_list = []
        for skill in eq.skills:
            skill_list.append(Skill(
                type=SkillType.SKILL,
                equipment=equipment,
                skill_id=skill.id,
                referenced_stat_type=skill.referencedStatType,
                stat_power_ratio=skill.statPowerRatio,
                power=skill.power,
                chance=skill.chance,
            ))
        for buff in eq.buffSkills:
            skill_list.append(Skill(
                type=SkillType.BUFF_SKILL,
                equipment=equipment,
                skill_id=buff.id,
                referenced_stat_type=buff.referencedStatType,
                stat_power_ratio=buff.statPowerRatio,
                power=buff.power,
                chance=buff.chance,
            ))
        equipment.all_skill_list = skill_list
        equipment_list.append(equipment)

    for cos in avatar_state_schema.inventory.costumes:
        costume = Costume(
            arena_info=arena_info,
            id=cos.itemId,
            sheet_id=cos.id,
            item_type=cos.itemType,
            item_subtype=cos.itemSubType,
            equipped=cos.itemId in equipped_items
        )
        costume_list.append(costume)

        if costume.equipped:
            if ItemSubType[costume.item_subtype] == ItemSubType.FULL_COSTUME:
                arena_info.costume_armor_id = costume.sheet_id
            elif ItemSubType[costume.item_subtype] == ItemSubType.TITLE:
                arena_info.title_id = costume.sheet_id

    arena_info.equipment_list = equipment_list
    arena_info.costume_list = costume_list
    arena_info.cp = CPCalculator(sess).get_cp(arena_info)
    sess.add(arena_info)
    # sess.commit()


def battle_arena(sess, data: BattleArena12Schema):
    # battle_arena12
    # update my avatar's equipments, costumes
    # update CP
    # update win/lose/score
    # update ranking(?)
    pass


def update_arena_info(sess, block_data: List[BlockSchema]):
    for block in block_data:
        print(f"Searching in block {block.index}...")
        for tx in block.transactions:
            for action in tx.actions:
                if action.type_id == "join_arena3":
                    print("join_arena found")
                    start = time()
                    join_arena(sess, action.values)
                    print(f"{time()-start} elapsed")
                if action.type_id == "battle_arena12":
                    # print("battle_arena found")
                    battle_arena(sess, action.values)
    sess.commit()
