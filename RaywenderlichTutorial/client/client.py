from PodSixNet.Connection import ConnectionListener

import config
from game import Game
from constants import Color

class Client(ConnectionListener):

    CONNECTING = "Connecting"
    WAITING_ON_PLAYER = "Waiting on player"
    IN_GAME = "In-game"
    DISCONNECTED = "Disconnected"

    def __init__(self, game: Game):
        # Start trying to connect.
        self.Connect((config.ip, config.port))
        self.state = Client.CONNECTING
        self.game: Game = game

    def Network(self, data):
        # This method is called when the incoming data has no action,
        # or an action that does not have a corresponding method
        print("Data Received: "+str(data))

    def Network_onJoined(self, data):
        # This means that this client was the first to join the game.
        # The game will not start until a second player has joined
        print("Joined game! Waiting for player 2.")
        self.state = Client.WAITING_ON_PLAYER

    def Network_disconnected(self, data: dict):
        self.state = Client.DISCONNECTED
        self.game.reset(Color.NONE)

    def Network_startGame(self, data: dict):
        # Two players have joined, the game may start now
        print("Data: "+str(data))

        # There is no guarantee that the incoming message is 
        # correctly formed.
        error = None

        if "color" in data:
            color = data["color"]
            if not (color == Color.BLUE or color == Color.RED):
                # It might have an unrecognized color
                error = f"Unrecognized color: {color}"
        else:
            # Or it might not have a color value at all
            error = "Missing data: color"

        if error is not None:
            print(error)
            self.state = Client.DISCONNECTED
            self.game.reset(Color.NONE)
        else:
            # If all goes well, reset the board
            # and start the game
            print("Game started!")
            self.state = Client.IN_GAME
            self.game.reset(color)

    def Network_placeLine(self, data):
        # Update the local copy of the board with info from the
        # server. Ignore the message if its format is unfamiliar.
        try:
            color = str(data["color"])
            i = int(data["i"])
            j = int(data["j"])
            horizontal = bool(int(data["horizontal"]))
        except ValueError as e:
            # A ValueError is expected if a conversion to int fails
            print("Unable to parse placeLine message: " + str(e))
            return
        except NameError: 
            # A NameError is expected if a key is missing
            print("Unable to parse placeLine message: " + str(e))
            return

        if not color in [Color.BLUE, Color.RED]:
            print("Unrecognized color: "+color)
            return

        if horizontal:
            limit = 5, 6
        else:
            limit = 6, 5

        if i < 0 or i > limit[0] or j < 0 or j > limit[1]:
            print("Index out of range")
            return

        self.game.place_line(i, j, horizontal, color)

    def Network_placeTile(self, data):
        # Update the local copy of the board with info from the
        # server. Ignore the message if its format is unfamiliar.
        try:
            color = str(data["color"])
            i = int(data["i"])
            j = int(data["j"])
        except ValueError as e:
            # A ValueError is expected if a conversion to int fails
            print("Unable to parse placeTile message: " + str(e))
            return
        except NameError: 
            # A NameError is expected if a key is missing
            print("Unable to parse placeTile message: " + str(e))
            return

        if not color in [Color.BLUE, Color.RED]:
            print("Unrecognized color: "+color)
            return

        if i < 0 or i > 5 or j < 0 or j > 5:
            print("Index out of range")
            return

        self.game.place_tile(i, j, color) 

    def Network_updateScore(self, data):
        # Update the local copy of the score with info from the
        # server. Ignore the message if its format is unfamiliar.
        try:
            local_score = int(data["localScore"])
            remote_score = int(data["remoteScore"])
        except ValueError as e:
            # A ValueError is expected if a conversion to int fails
            print("Unable to parse localScore message: " + str(e))
            return
        except NameError: 
            # A NameError is expected if a key is missing
            print("Unable to parse localScore message: " + str(e))
            return

        if local_score < 0:
            print("Local score out of range:", local_score)
            return

        if remote_score < 0:
            print("Remote score out of range", remote_score)

        self.game.update_score(local_score, remote_score) 