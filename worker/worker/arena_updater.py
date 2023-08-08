import json
import os
import random
from collections import defaultdict
from typing import List
from uuid import UUID

from common import logger
from common.const import HOST_DICT
from common.enums import SkillType, ItemSubType
from common.models.arena import Arena
from common.models.avatar import ArenaInfo, Costume, Equipment, Skill, EquipmentStat
from common.schemas.avatar import AvatarStateSchema
from common.schemas.block import BlockSchema
from common.utils.cp import CPCalculator
from common.utils.gql import execute_gql
from sqlalchemy import select

stage = os.environ.get("STAGE", "development")
HOST = random.choice(HOST_DICT[stage])
JOIN_ARENA_ACTION = {"join_arena3", }
BATTLE_ARENA_ACTION = {"battle_arena12", }


def decode_item_id(encoded: str) -> str:
    bs = bytes.fromhex(encoded[2:])
    return str(UUID(bytes_le=bs))


def get_avatar_state(avatar_addr_list: List[str]) -> List[AvatarStateSchema]:
    query = f"""{{
    stateQuery {{
        avatars (
            avatarAddresses: {json.dumps(avatar_addr_list)}
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
    return [AvatarStateSchema(**x) for x in resp["stateQuery"]["avatars"] if x is not None]


def join_arena(sess, block: BlockSchema):
    data_dict = defaultdict(dict)
    equipped_items = set()
    for tx in block.transactions:
        for action in tx.actions:
            if action.type_id in JOIN_ARENA_ACTION:
                # Separate action data by championship-round
                data_dict[(action.values.championshipId, action.values.round)][
                    action.values.avatarAddress] = action.values
                # All item ids are unique, so we can handle them at once
                equipped_items |= {decode_item_id(x) for x in (action.values.equipments + action.values.costumes)}

    for (championship, round), address_dict in data_dict.items():
        # Cut invalid arena
        target_arena = sess.scalar(
            select(Arena).where(Arena.championship == championship, Arena.round == round)
        )
        if not target_arena:
            msg = f"There is no Arena of Championship {championship} Round {round}"
            logger.error(msg)
            continue
            # raise ValueError(msg)

        # Cut previously joined avatars
        prev_info = sess.scalars(
            select(ArenaInfo.avatar_addr)
            .where(ArenaInfo.arena_id == target_arena.id, ArenaInfo.avatar_addr.in_(list(address_dict.keys())))
        ).fetchall()
        for prev in prev_info:
            del address_dict[prev]
        logger.info(f"{len(address_dict)} new avatars joined to the arena")
        if not address_dict:
            continue

        # Get all avatar states
        avatar_state_schema_list = get_avatar_state(list(address_dict.keys()))
        for avatar_state_schema in avatar_state_schema_list:
            data = address_dict[avatar_state_schema.address.lower()]
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
                if eq.itemId not in equipped_items:
                    continue

                equipment = Equipment(
                    arena_info=arena_info,
                    item_id=eq.itemId,
                    sheet_id=eq.id,
                    item_type=eq.itemType,
                    item_subtype=eq.itemSubType,
                    elemental_type=eq.elementalType,
                    level=eq.level,
                    set_id=eq.setId,
                    stat_type=eq.stat.statType,
                    stat_value=eq.stat.totalValue,
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
                if cos.itemId not in equipped_items:
                    continue

                costume = Costume(
                    arena_info=arena_info,
                    item_id=cos.itemId,
                    sheet_id=cos.id,
                    item_type=cos.itemType,
                    item_subtype=cos.itemSubType,
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


def battle_arena(sess, block: BlockSchema):
    # battle_arena12
    # update my avatar's equipments, costumes
    # update CP
    # update win/lose/score
    # update ranking(?)
    pass


def update_arena_info(sess, block_data: List[BlockSchema]):
    for block in block_data:
        print(f"Searching in block {block.index}...")
        action_set = set()
        for tx in block.transactions:
            for action in tx.actions:
                action_set.add(action.type_id)

        if action_set & JOIN_ARENA_ACTION:
            join_arena(sess, block)
        if action_set & BATTLE_ARENA_ACTION:
            battle_arena(sess, block)

            # if action.type_id == "join_arena3":
            #     print("join_arena found")
            #     start = time()
            #     join_arena(sess, action.values)
            #     print(f"{time() - start} elapsed")
            # if action.type_id == "battle_arena12":
            #     # print("battle_arena found")
            #     battle_arena(sess, action.values)
    # sess.commit()
