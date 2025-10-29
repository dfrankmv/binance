from utils import *

@dataclass
class Balance:
    asset: str
    free: float
    locked: float