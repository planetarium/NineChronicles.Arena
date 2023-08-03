from dataclasses import dataclass
from typing import Dict, Any, Union, List


class BaseActionValueSchema:
    pass


@dataclass
class PatchTableSheetSchema(BaseActionValueSchema):
    id: str
    table_name: str
    table_csv: str


@dataclass
class JoinArena3Schema(BaseActionValueSchema):
    id: str
    championshipId: int
    round: int
    avatarAddress: str
    costumes: List[str]
    equipments: List[str]
    runeInfos: List[List[str]]


@dataclass
class BattleArena12Schema(BaseActionValueSchema):
    id: str
    chi: int  # Championship ID
    rd: int  # Round
    maa: str  # My avatar address
    cs: List  # Costumes
    es: List[str]  # Equipments
    ri: List[List[str]]  # Rune infos
    eaa: str  # Enemy avatar address
    tk: int  # Ticket


@dataclass
class ActionSchema:
    type_id: str
    values: Union[Dict[str, Any], BaseActionValueSchema]

    def __post_init__(self):
        if type(self.values) != BaseActionValueSchema:
            schema_name = f'{"".join([x.capitalize() for x in self.type_id.split("_")])}Schema'
            cls = globals().get(schema_name)
            if cls:
                self.values = cls(**self.values)
