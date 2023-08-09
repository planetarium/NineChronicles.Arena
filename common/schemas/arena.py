from dataclasses import dataclass


@dataclass
class ArenaInformationSchema:
    avatarAddress: str
    address: str
    win: int
    lose: int
    score: int
    ticket: int
    ticketResetCount: int
    purchasedTicketCount: int
