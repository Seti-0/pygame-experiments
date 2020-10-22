# This game was made for learning purposes,
# hence the abundance of unnecessary comments
# all over the place

import time
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from server import BoxesServer

print("Starting server on localhost")
server = BoxesServer(localaddr=("localhost", 8888))

while True:
    server.Pump()
    time.sleep(0.01)