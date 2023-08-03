import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Union, List, Dict, Any

from common.schemas.action import ActionSchema


@dataclass
class TxSchema:
    actions: Union[List[Dict[str, str]], List[ActionSchema]]
    transformed: bool = False

    def __post_init__(self):
        if not self.transformed:
            action_list = []
            for action in self.actions:
                sanitized = action["json"].replace("\\uFEFF", "")
                action_list.append(ActionSchema(**json.loads(sanitized)))
            self.actions = action_list
            self.transformed = True


@dataclass
class BlockSchema:
    index: int
    hash: str
    timestamp: Union[str, datetime]
    transactions: Union[List[Dict[str, Any]], List[TxSchema]]

    def __post_init__(self):
        dt, ms, tz = re.split(r"[.+]", self.timestamp)
        if len(ms) != 6:
            ms = f"{ms}{'0'*(6-len(ms))}"
        self.timestamp = f"{dt}.{ms}+{tz}"
        self.timestamp = datetime.fromisoformat(self.timestamp)
        self.transactions = [TxSchema(**x) for x in self.transactions]
