from utils import *

@dataclass
class API:
    method: str
    path  : str
    signed: bool = True
    keyed : bool = True

    class Exception(Exception): pass
    
    class APIKeyFormatInvalidException(Exception): pass
    class InvalidListenKeyException(Exception): pass
    class ListenKeyExpiredException(Exception): pass
    class ListenKeyNotSentException(Exception): pass