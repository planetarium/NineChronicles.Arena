from dataclasses import dataclass
from typing import Optional


@dataclass
class ArenaInformationSchema:
    avatarAddress: str
    address: Optional[str]
    win: Optional[int]
    lose: Optional[int]
    score: Optional[int]
    ticket: Optional[int]
    ticketResetCount: Optional[int]
    purchasedTicketCount: Optional[int]
