from utils import *

from ..enums import *

@dataclass
class Order:
    cid    : str   = None # CLIENT/CUSTOM ID
    tid    : str   = None # TRADER ID
    gid    : str   = None # GROUP ID
    xid    : int   = None # EXCHANGE ID
    status : str   = None 
    pair   : str   = None  
    action : int   = None  
    ctype  : str   = None # CLIENT/CUSTOM TYPE
    xtype  : str   = None # EXCHANGE TYPE
    qty    : float = None  
    price  : float = None  
    side   : int   = None  
    stop   : float = None # STOP/ACTIVATION PRICE
    delta  : float = None # TRAILING DELTA

    def is_completed(self): 
        return self.status not in [STATUS.NEW, STATUS.PARTIALLY_FILLED]

    def is_filled(self):
        return self.status == STATUS.FILLED
    
    def is_new(self):
        return self.status == STATUS.NEW
    
    def is_canceled(self):
        return self.status == STATUS.CANCELED
    
    def is_market_trailing(self):
        return self.ctype == CTYPE.MARKET_TRAILING
    
    def is_limit_trailing(self):
        return self.ctype == CTYPE.LIMIT_TRAILING
    
    def is_buy(self):
        return self.action == ACTION.BUY
    
    def is_sell(self):
        return self.action == ACTION.SELL
    
    def is_long(self):
        return self.side == SIDE.LONG
    
    def is_short(self):
        return self.side == SIDE.SHORT
    
    def is_increase(self):
        return self.action == self.side
    
    def is_decrease(self):
        return self.action == -self.side