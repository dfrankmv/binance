from ._client import *

class Futures(Client):
    base_api_url = "https://fapi.binance.com"
    base_ws_url  = "wss://fstream.binance.com/ws"



    # ------------- #
    # API ENDPOINTS #
    # ------------- #

    api_create_listen_key = API("POST", "/fapi/v1/listenKey", False)
    api_ping_listen_key   = API("PUT", "/fapi/v1/listenKey", False)
    api_delete_listen_key = API("DELETE", "/fapi/v1/listenKey", False)



    # --------- #
    # API CALLS #
    # --------- #

    def delete_listen_key(self, listen_key:str=""):
        self.invoke_api(self.api_delete_listen_key)

    def ping_listen_key(self, listen_key:str=""):
        res = self.invoke_api(self.api_ping_listen_key)
        if res["listenKey"] != listen_key:
            raise API.InvalidListenKeyException("This listenKey does not exist.")



    def x2ctype(self, xtype:str):
        match xtype:
            case "MARKET": return CTYPE.MARKET
            case "LIMIT": return CTYPE.LIMIT
            case "STOP_MARKET": return CTYPE.STOP_MARKET
            case "STOP": return CTYPE.STOP_LIMIT
            case "TAKE_PROFIT_MARKET": return CTYPE.STOP_MARKET
            case "TAKE_PROFIT": return CTYPE.STOP_LIMIT
            case "TRAILING_STOP_MARKET": return CTYPE.TRAILING



    # ----------------------- #
    # USOCKET RELATED METHODS #
    # ----------------------- #

    def umsg2event(self, umsg:str):
        jmsg = json.loads(umsg)
        match jmsg["e"]:
            case "listenKeyExpired":
                raise API.ListenKeyExpiredException
            case "ORDER_TRADE_UPDATE":
                omsg = dict(jmsg["o"])
                return OrderUpdated(jmsg["E"], Order(
                    cid = omsg["c"],
                    xid = omsg["i"],
                    status = omsg["X"],
                    pair = omsg["s"],
                    action = ACTION[omsg["S"]],
                    ctype = self.x2ctype(omsg["o"]),
                    xtype = omsg["o"],
                    qty = float(omsg["q"]),
                    price = float(omsg["p"]) or None,
                    side = SIDE[omsg["ps"]],
                    stop = float(omsg.get("AP", 0)) or float(omsg["sp"]) or None,
                    delta = float(omsg.get("cr", 0)) or None,
                ))
            case other:
                print(jmsg)

        

# {"e": "listenKeyExpired","E": "1761017175473","listenKey": "3iAIYPTyyKLahCRIdJuDqPltJ77hOa82B8i4cWNgXs6plqKHaizNMzShYqzTvlJF"}

""" 
{
    "e": "ORDER_TRADE_UPDATE",
    "T": 1761108748987,
    "E": 1761108748988,
    "o": {
        "s": "SOLUSDT",
        "c": "x-VLi5VFhX-tp-1691713",
        "S": "BUY",
        "o": "LIMIT",
        "f": "GTC",
        "q": "0.05",
        "p": "178.34",
        "ap": "0",
        "sp": "0",
        "x": "CANCELED",
        "X": "CANCELED",
        "i": 160846448049,
        "l": "0",
        "z": "0",
        "L": "0",
        "n": "0",
        "N": "USDT",
        "T": 1761108748987,
        "t": 0,
        "b": "9.408299",
        "a": "0",
        "m": False,
        "R": False,
        "wt": "CONTRACT_PRICE",
        "ot": "LIMIT",
        "ps": "LONG",
        "cp": False,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}
"""