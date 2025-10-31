PUBLIC_KEY = "YOUR_PUBLIC_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"

from binance import *

# CLIENT CAN BE FUTURES, SPOT, OR MARGIN
c = Futures(PUBLIC_KEY, SECRET_KEY)

# USOCKET TO LISTEN USER EVENTS
u = USocket(c)

# START USOCKET
u.start()

# HANDLE EVENTS
for ev in u.next_event():
    print(ev)