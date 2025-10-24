from ..models import *

class Client(ABC):
    base_api_url: str
    base_ws_url : str

    api_create_listen_key: API
    api_ping_listen_key  : API
    api_delete_listen_key: API

    def delete_listen_key(self, listen_key:str=""):
        raise NotImplementedError
    
    def ping_listen_key(self, listen_key:str=""):
        raise NotImplementedError

    def __init__(self, public_key:str, secret_key:str):
        self.public_key = public_key
        self.secret_key = secret_key

    def invoke_api(self, api:API, params:dict=None):
        url = f"{self.base_api_url}{api.path}"
        hdr = {"X-MBX-APIKEY": self.public_key} if api.keyed else None
        res = requests.request(api.method, url, params=params, headers=hdr)
        match res.status_code:
            case 400:
                match res.json()["code"]:
                    case -1125: raise API.InvalidListenKeyException(res.text)
                    case -1102: raise API.ListenKeyNotSentException(res.text)
                    case -1105: raise API.ListenKeyNotSentException(res.text)
                    case _    : raise API.Exception(res.text)
            case 401:
                match res.json()["code"]:
                    case -2014: raise API.APIKeyFormatInvalidException(res.text)
                    case _    : raise API.Exception(res.text)
        return dict(res.json())

    def create_listen_key(self):
        res = self.invoke_api(self.api_create_listen_key)
        return str(res["listenKey"])

    

    # ----------------------- #
    # USOCKET RELATED METHODS #
    # ----------------------- #

    def umsg2event(self, umsg:str) -> Event:
        raise NotImplementedError