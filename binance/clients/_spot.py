from ._client import *

class Spot(Client):
    base_api_url = "https://api.binance.com"
    base_ws_url = "wss://stream.binance.com:9443/ws"



    # ------------- #
    # API ENDPOINTS #
    # ------------- #

    api_account_information    = API("GET", "/api/v3/account")
    api_all_orders             = API("GET", "/api/v3/allOrders")
    api_cancel_replace_order   = API("POST", "/api/v3/order/cancelReplace")
    api_cancel_order           = API("DELETE", "/api/v3/order")
    api_create_listen_key      = API("POST", "/api/v3/userDataStream", False, True)
    api_delete_listen_key      = API("DELETE", "/api/v3/userDataStream", False, True)
    api_exchange_information   = API("GET", "/api/v3/exchangeInfo", False, False)
    api_get_bnb_burn_status    = API("GET", "/sapi/v1/bnbBurn")
    api_modify_bnb_burn_status = API("POST", "/sapi/v1/bnbBurn")
    api_my_trades              = API("GET", "/api/v3/myTrades")
    api_new_order              = API("POST", "/api/v3/order")
    api_open_orders            = API("GET", "/api/v3/openOrders")
    api_ping_listen_key        = API("PUT", "/api/v3/userDataStream", False, True)
    api_query_order            = API("GET", "/api/v3/order")
    api_symbol_price_ticker    = API("GET", "/api/v3/ticker/price", False, False)
    api_time                   = API("GET", "/api/v1/time", False, False)
    api_transfer               = API("POST", "/sapi/v1/asset/transfer")
    api_user_assets            = API("POST", "/sapi/v3/asset/getUserAsset")
    api_klines                 = API("GET", "/api/v3/klines", False, False)



    # --------- #
    # API CALLS #
    # --------- #

    def delete_listen_key(self, listen_key:str=""):
        self.invoke_api(self.api_delete_listen_key, {
            "listenKey": listen_key
        })

    def ping_listen_key(self, listen_key:str=""):
        self.invoke_api(self.api_ping_listen_key, {
            "listenKey": listen_key
        })

    def x2ctype(self, xtype:str):
        match xtype:
            case "LIMIT": return CTYPE.LIMIT
            case "MARKET": return CTYPE.MARKET
            case "STOP_LOSS": return CTYPE.STOP_MARKET
            case "STOP_LOSS_LIMIT": return CTYPE.STOP_LIMIT
            case "TAKE_PROFIT": return CTYPE.STOP_MARKET
            case "TAKE_PROFIT_LIMIT": return CTYPE.STOP_LIMIT

    # ----------------------- #
    # USOCKET RELATED METHODS #
    # ----------------------- #

    def umsg2event(self, umsg:str):
        jmsg = dict(json.loads(umsg))
        match jmsg["e"]:
            case "outboundAccountPosition":
                return AccountUpdated(jmsg["E"], [Balance(b["a"], b["f"], b["l"]) for b in jmsg["B"]])
            case "executionReport":
                delta = jmsg.get("d", 0.0)/100.0 or None
                ctype = CTYPE.TRAILING if delta else self.x2ctype(jmsg["o"])
                return OrderUpdated(jmsg["E"], Order(
                    cid = jmsg["C"] or jmsg["c"],
                    xid = jmsg["i"],
                    status = jmsg["X"],
                    pair = jmsg["s"],
                    action = ACTION[jmsg["S"]],
                    ctype = ctype,
                    xtype = jmsg["o"],
                    qty = float(jmsg["q"]),
                    price = float(jmsg["p"]) or float(jmsg["L"]) or None,
                    side = None,
                    stop = float(jmsg["P"]) or None,
                    delta = delta,
                ))
            case other:
                print(jmsg)
                # raise EventException



""" 
{
    "e": "executionReport",
    "E": 1761101867881,
    "s": "SOLUSDT",
    "c": "ThdzmGIooPGm9SiiVwgiBX",
    "S": "BUY",
    "o": "LIMIT",
    "f": "GTC",
    "q": "0.13800000",
    "p": "179.62000000",
    "P": "0.00000000",
    "F": "0.00000000",
    "g": -1,
    "C": "x-SGZ1QV0A-tp-1691556",
    "x": "CANCELED",
    "X": "CANCELED",
    "r": "NONE",
    "i": 14860443618,
    "l": "0.00000000",
    "z": "0.00000000",
    "L": "0.00000000",
    "n": "0",
    "N": null,
    "T": 1761101867880,
    "t": -1,
    "I": 31859517501,
    "w": false,
    "m": false,
    "M": false,
    "O": 1761101833247,
    "Z": "0.00000000",
    "Y": "0.00000000",
    "Q": "0.00000000",
    "W": 1761101833247,
    "V": "EXPIRE_MAKER"
}
"""




"""
{
    "e": "outboundAccountPosition",
    "E": 1761073967329,
    "u": 1761073967329,
    "B": [
        {
            "a": "BNB",
            "f": "0.06176431",
            "l": "0.00000000"
        },
        {
            "a": "USDT",
            "f": "110.99960380",
            "l": "9.98792000"
        },
        {
            "a": "SOL",
            "f": "0.01882400",
            "l": "0.00000000"
        }
    ]
}
"""


