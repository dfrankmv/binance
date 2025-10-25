from ..clients import *

class USocket(Multiton):
    ws: WebSocketApp

    def __init__(self, client:Client):
        self.client = client
        self._events = Queue[dict]()
    
    def on_open(self, ws:WebSocketApp):
        self.reconnect_timeout_seconds = 1
        log("USOCKET_OPEN", "Connection opened.")

    def on_error(self, ws:WebSocketApp, error:Exception):
        log("USOCKET_ERROR", f"Error: {error}")
        
    def on_close(self, ws:WebSocketApp, code:int, msg:str):
        log("USOCKET_CLOSE", f"Connection closed (code = {code}, msg = {msg})")
        log("USOCKET_CLOSE", f"Reconnecting after {self.reconnect_timeout_seconds} seconds...")
        time.sleep(self.reconnect_timeout_seconds)
        self.reconnect_timeout_seconds *= 2
        self.t_connect()

    def on_ping(self, ws:WebSocketApp, payload:bytes):
        ws.sock.pong(payload)

    def on_message(self, ws:WebSocketApp, umsg:str):
        Logger("usocket").info("USOCKET_MESSAGE", umsg)
        try:
            event = self.client.umsg2event(umsg)
            self._events.put(event)
        except API.ListenKeyExpiredException:
            ws.close()

    @run_in_thread
    def t_keep_alive(self, ping_every_seconds:int):
        while True:
            try:
                time.sleep(ping_every_seconds)
                # TODO LOG PING
                self.client.ping_listen_key(self.listen_key)
            except API.InvalidListenKeyException:
                self.ws.close()

    @run_in_thread
    def t_connect(self):
        self.listen_key = self.client.create_listen_key()
        self.ws = WebSocketApp(f"{self.client.base_ws_url}/{self.listen_key}")
        self.ws.on_open = self.on_open
        self.ws.on_error = self.on_error
        self.ws.on_close = self.on_close
        self.ws.on_ping = self.on_ping
        self.ws.on_message = self.on_message
        self.ws.run_forever()

    def run(self, ping_every_seconds:int=33):
        self.reconnect_timeout_seconds = 1
        self.t_connect()
        self.t_keep_alive(ping_every_seconds)

    def next_event(self):
        while True:
            yield self._events.get()

if __name__ == "__main__":
    from api_keys import *
    
    with helpers.run_until_interrupt():
        c = Futures(PUBLIC_KEY, SECRET_KEY)
        u = USocket(c)
        u.run(5)
        for ev in u.next_event():
            print(ev)
            print()