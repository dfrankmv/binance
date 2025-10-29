from ._balance import *
from ._order import *

class EventException(Exception): 
    pass

@dataclass
class Event:
    timestamp: int

@dataclass
class AccountUpdated(Event):
    balances: list[Balance]

@dataclass
class OrderUpdated(Event):
    order: Order