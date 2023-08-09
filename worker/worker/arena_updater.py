import json
import os
import random
from collections import defaultdict
from typing import List, Dict
from uuid import UUID

from common import logger
from common.const import HOST_DICT
from common.enums import SkillType, ItemSubType
from common.models.arena import Arena
from common.models.avatar import ArenaInfo, Costume, Equipment, Skill, EquipmentStat, Rune
from common.schemas.arena import ArenaInformationSchema
from common.schemas.avatar import AvatarStateSchema
from common.schemas.block import BlockSchema
from common.utils.cp import CPCalculator
from common.utils.gql import execute_gql
from sqlalchemy import select

stage = os.environ.get("STAGE", "development")
HOST = random.choice(HOST_DICT[stage])
JOIN_ARENA_ACTION = {"join_arena3", }
BATTLE_ARENA_ACTION = {"battle_arena12", }
TARGET_ACTION_LIST = JOIN_ARENA_ACTION | BATTLE_ARENA_ACTION


def decode_item_id(encoded: str) -> str:
    bs = bytes.fromhex(encoded[2:])
    return str(UUID(bytes_le=bs))


def get_avatar_state(avatar_addr_list: List[str]) -> List[AvatarStateSchema]:
    query = f"""{{
    stateQuery {{
        avatars (
            addresses: {json.dumps(avatar_addr_list)}
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
            runes {{
                runeId level
            }}
        }}
    }}
    }}
    """
    resp = execute_gql(f"{HOST}/graphql", query)
    return [AvatarStateSchema(**x) for x in resp["stateQuery"]["avatars"] if x is not None]


def get_arena_state(championship: int, round: int, avatar_addr_list: List[str]) -> List[ArenaInformationSchema]:
    query = f"""{{
        stateQuery {{
            arenaInformation(
                championshipId: {championship}
                round: {round}
                avatarAddresses: {json.dumps(avatar_addr_list)}
            ) {{
                avatarAddress
                address
                win
                lose
                score
                ticket
                ticketResetCount
                purchasedTicketCount
            }}
        }}
    }}"""
    resp = execute_gql(f"{HOST}/graphql", query)
    return [ArenaInformationSchema(**x) for x in resp["stateQuery"]["arenaInformation"] if x is not None]


def update_arena_info(sess, block: BlockSchema):
    data_dict = defaultdict(dict)
    equipped_items = set()
    for tx in block.transactions:
        for action in tx.actions:
            if action.type_id in TARGET_ACTION_LIST:
                # Separate action data by championship-round
                data_dict[(action.values.championshipId, action.values.round, action.type_id)][
                    action.values.avatarAddress] = action.values
                # All item ids are unique, so we can handle them at once
                equipped_items |= {decode_item_id(x) for x in (action.values.equipments + action.values.costumes)}

    for (championship, round, action_type), action_dict in data_dict.items():
        # Cut invalid arena
        target_arena = sess.scalar(
            select(Arena).where(Arena.championship == championship, Arena.round == round)
        )
        if not target_arena:
            msg = f"There is no Arena of Championship {championship} Round {round}"
            logger.error(msg)
            continue

        arena_dict: Dict[str, ArenaInfo] = {
            x.avatar_addr: x for x in sess.scalars(
                select(ArenaInfo)
                .where(ArenaInfo.arena_id == target_arena.id, ArenaInfo.avatar_addr.in_(list(action_dict.keys())))
            ).fetchall()
        }
        if action_type in JOIN_ARENA_ACTION:
            # Remove prev. joined avatars
            action_dict = {k: v for k, v in action_dict.items() if k not in arena_dict}
            logger.info(f"{len(action_dict)} new avatars joined to the arena")
            if not action_dict:
                continue
        else:  # BATTLE_ARENA_ACTION
            # Remove not joined avatars
            action_dict = {k: v for k, v in action_dict.items() if k in arena_dict}
            logger.info(f"{len(action_dict)} avatars battled in the arena")
            if not action_dict:
                continue

        avatar_state_dict = {x.address: x for x in get_avatar_state(list(action_dict.keys()))}
        arena_state_dict = {x.avatarAddress: x for x in get_arena_state(championship, round, list(action_dict.keys()))}

        for addr, action_value in action_dict.items():
            arena_info = arena_dict.get(addr.lower())
            avatar_state = avatar_state_dict[addr.lower()]
            arena_state = arena_state_dict.get(addr.lower())
            if not arena_info:
                # JoinArena
                arena_info = ArenaInfo(
                    avatar_addr=action_value.avatarAddress,
                    arena_id=target_arena.id,
                    agent_addr=avatar_state.agentAddress,
                    name=avatar_state.name,
                    level=avatar_state.level,
                    character_id=avatar_state.characterId,
                )

            # Apply arena result
            if arena_state:
                arena_info.update_arena_info(arena_state)

            # Update avatar state
            equipment_list = []
            costume_list = []

            for eq in avatar_state.inventory.equipments:
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

            for cos in avatar_state.inventory.costumes:
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

                if ItemSubType[costume.item_subtype] == ItemSubType.FULL_COSTUME:
                    arena_info.costume_armor_id = costume.sheet_id
                elif ItemSubType[costume.item_subtype] == ItemSubType.TITLE:
                    arena_info.title_id = costume.sheet_id

            equipped_runes = [x[1] for x in action_value.runeInfos]
            rune_list = []
            for rune in avatar_state.runes:
                if rune.runeId not in equipped_runes:
                    continue
                rune_list.append(
                    Rune(
                        arena_info=arena_info,
                        rune_id=rune.runeId,
                        level=rune.level
                    )
                )

            arena_info.equipment_list = equipment_list
            arena_info.costume_list = costume_list
            arena_info.rune_list = rune_list
            arena_info.cp = CPCalculator(sess).get_cp(arena_info)
            sess.add(arena_info)


def apply_arena_actions(sess, block_data: List[BlockSchema]):
    for block in block_data:
        print(f"Searching in block {block.index}...")
        action_set = set()
        for tx in block.transactions:
            for action in tx.actions:
                action_set.add(action.type_id)

        if action_set & TARGET_ACTION_LIST:
            update_arena_info(sess, block)

    # sess.commit()
