import random
from typing import List

from common.schemas.arena import ArenaInformationSchema
from common.schemas.avatar import AvatarStateSchema


def mock_get_avatar_state(avatar_addr_list: List[str]) -> List[AvatarStateSchema]:
    return [AvatarStateSchema(
        **{
            "address": "0x211939355049999363383840912",
            "agentAddress": "0x81291023468377205534914161158",
            "name": "monkeypatch",
            "level": 316,
            "characterId": 100010,
            "inventory": {
                "equipments": [
                    {
                        "id": 10151000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "WEAPON",
                        "elementalType": "FIRE",
                        "level": 4,
                        "itemId": "7a1840ac-ff48-4d5d-9c94-50664d80f534",
                        "setId": 17,
                        "equipped": True,
                        "stat": {
                            "statType": "ATK",
                            "totalValue": 4331
                        },
                        "skills": [
                            {
                                "id": 260000,
                                "referencedStatType": "ATK",
                                "statPowerRatio": 3118,
                                "power": 0,
                                "chance": 32
                            }
                        ],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 15857,
                            "aTK": 12286,
                            "dEF": 0,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10152000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "WEAPON",
                        "elementalType": "WATER",
                        "level": 0,
                        "itemId": "881f4134-bb0d-46c8-b688-e3161ac80b7f",
                        "setId": 18,
                        "equipped": False,
                        "stat": {
                            "statType": "ATK",
                            "totalValue": 4331
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 0,
                            "aTK": 6493,
                            "dEF": 998,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10152000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "WEAPON",
                        "elementalType": "WATER",
                        "level": 0,
                        "itemId": "5c8678ec-a8ab-42f8-bd0b-7f616a95be1c",
                        "setId": 18,
                        "equipped": False,
                        "stat": {
                            "statType": "ATK",
                            "totalValue": 4331
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 0,
                            "aTK": 6517,
                            "dEF": 1047,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10351001,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "BELT",
                        "elementalType": "FIRE",
                        "level": 3,
                        "itemId": "9a697a2e-6a5c-4316-b59b-717725d6e15c",
                        "setId": 15,
                        "equipped": True,
                        "stat": {
                            "statType": "SPD",
                            "totalValue": 10267
                        },
                        "skills": [
                            {
                                "id": 220005,
                                "referencedStatType": "ATK",
                                "statPowerRatio": 4177,
                                "power": 0,
                                "chance": 8
                            }
                        ],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 0,
                            "aTK": 2138,
                            "dEF": 0,
                            "cRI": 0,
                            "sPD": 22262
                        }
                    },
                    {
                        "id": 10454001,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "NECKLACE",
                        "elementalType": "WIND",
                        "level": 0,
                        "itemId": "960ac7d8-de3c-4ffe-9a3c-af9a4d6cf17e",
                        "setId": 15,
                        "equipped": True,
                        "stat": {
                            "statType": "HIT",
                            "totalValue": 15363
                        },
                        "skills": [
                            {
                                "id": 300002,
                                "referencedStatType": "HP",
                                "statPowerRatio": 486,
                                "power": 0,
                                "chance": 8
                            }
                        ],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 24994,
                            "aTK": 2571,
                            "dEF": 0,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10550000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "RING",
                        "elementalType": "NORMAL",
                        "level": 0,
                        "itemId": "1013d815-0f9c-4dd5-92af-20b43d0c273c",
                        "setId": 11,
                        "equipped": True,
                        "stat": {
                            "statType": "DEF",
                            "totalValue": 1946
                        },
                        "skills": [
                            {
                                "id": 110006,
                                "referencedStatType": "ATK",
                                "statPowerRatio": 18144,
                                "power": 0,
                                "chance": 8
                            }
                        ],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 4882,
                            "aTK": 0,
                            "dEF": 4172,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10553000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "RING",
                        "elementalType": "LAND",
                        "level": 2,
                        "itemId": "e3f2d79e-bd57-4b9f-a84d-187f75fcd177",
                        "setId": 14,
                        "equipped": True,
                        "stat": {
                            "statType": "DEF",
                            "totalValue": 1946
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 31344,
                            "hIT": 0,
                            "aTK": 8247,
                            "dEF": 4858,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10141000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "WEAPON",
                        "elementalType": "FIRE",
                        "level": 1,
                        "itemId": "446c8eca-c582-4550-8cfe-84c3e89eaff6",
                        "setId": 12,
                        "equipped": False,
                        "stat": {
                            "statType": "ATK",
                            "totalValue": 1934
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 0,
                            "aTK": 2785,
                            "dEF": 0,
                            "cRI": 0,
                            "sPD": 3051
                        }
                    },
                    {
                        "id": 10240000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "ARMOR",
                        "elementalType": "NORMAL",
                        "level": 6,
                        "itemId": "1d5384bf-863d-44ce-9eaa-5b88dd9d5f3e",
                        "setId": 11,
                        "equipped": True,
                        "stat": {
                            "statType": "HP",
                            "totalValue": 34446
                        },
                        "skills": [
                            {
                                "id": 220000,
                                "referencedStatType": "NONE",
                                "statPowerRatio": 0,
                                "power": 0,
                                "chance": 9
                            }
                        ],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 90829,
                            "hIT": 0,
                            "aTK": 0,
                            "dEF": 1009,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10242000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "ARMOR",
                        "elementalType": "WATER",
                        "level": 0,
                        "itemId": "a53bf69e-d531-4e74-b423-721a4e92528b",
                        "setId": 13,
                        "equipped": False,
                        "stat": {
                            "statType": "HP",
                            "totalValue": 27064
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 34684,
                            "hIT": 0,
                            "aTK": 0,
                            "dEF": 0,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10541000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "RING",
                        "elementalType": "FIRE",
                        "level": 0,
                        "itemId": "b44a1c62-0a8f-4bbb-99c1-ff000922068e",
                        "setId": 12,
                        "equipped": False,
                        "stat": {
                            "statType": "DEF",
                            "totalValue": 540
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 0,
                            "aTK": 603,
                            "dEF": 766,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10544000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "RING",
                        "elementalType": "WIND",
                        "level": 5,
                        "itemId": "8fa8ac47-aa6b-4a5c-a59c-653a9a6ab1d7",
                        "setId": 15,
                        "equipped": False,
                        "stat": {
                            "statType": "DEF",
                            "totalValue": 783
                        },
                        "skills": [
                            {
                                "id": 140005,
                                "referencedStatType": "NONE",
                                "statPowerRatio": 0,
                                "power": 41463,
                                "chance": 10
                            }
                        ],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 0,
                            "aTK": 0,
                            "dEF": 2686,
                            "cRI": 0,
                            "sPD": 0
                        }
                    },
                    {
                        "id": 10511000,
                        "itemType": "EQUIPMENT",
                        "itemSubType": "RING",
                        "elementalType": "FIRE",
                        "level": 8,
                        "itemId": "373bd8e3-c327-412d-94fd-ecd0a3a333f5",
                        "setId": 2,
                        "equipped": False,
                        "stat": {
                            "statType": "DEF",
                            "totalValue": 9
                        },
                        "skills": [],
                        "buffSkills": [],
                        "statsMap": {
                            "hP": 0,
                            "hIT": 1692,
                            "aTK": 1047,
                            "dEF": 19,
                            "cRI": 0,
                            "sPD": 0
                        }
                    }
                ],
                "costumes": [
                    {
                        "id": 40100010,
                        "itemType": "COSTUME",
                        "itemSubType": "FULL_COSTUME",
                        "itemId": "989dfe65-b201-4e55-a7c9-a90edf82abe0",
                        "equipped": False
                    },
                    {
                        "id": 40100011,
                        "itemType": "COSTUME",
                        "itemSubType": "FULL_COSTUME",
                        "itemId": "bba57215-ee6f-4678-a0fb-0a2a76e5589c",
                        "equipped": True
                    },
                    {
                        "id": 49900007,
                        "itemType": "COSTUME",
                        "itemSubType": "TITLE",
                        "itemId": "066c66d4-c49f-4e3e-8fa2-78d85f6cdcab",
                        "equipped": True
                    }
                ],
            },
            "runes": [
                {
                    "runeId": 10001,
                    "level": 9
                },
                {
                    "runeId": 10002,
                    "level": 79
                },
                {
                    "runeId": 10003,
                    "level": 42
                },
                {
                    "runeId": 10011,
                    "level": 52
                },
                {
                    "runeId": 10012,
                    "level": 78
                },
                {
                    "runeId": 10013,
                    "level": 40
                },
                {
                    "runeId": 20001,
                    "level": 10
                },
                {
                    "runeId": 30001,
                    "level": 117
                }
            ]
        }
    )]


def mock_get_arena_information(championship: int, round: int, avatar_addr_list: List[str]) -> List[ArenaInformationSchema]:
    return [
        ArenaInformationSchema(
            avatarAddress="0x211939355049999363383840912",
            address="0x001",
            win=random.choice(range(10)),
            lose=random.choice(range(10)),
            score=random.choice(range(500, 2000)),
            ticket=random.choice(range(9)),
            ticketResetCount=random.choice(range(20)),
            purchasedTicketCount=random.choice(range(10))
        )
    ]
