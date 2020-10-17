# This game was made for learning purposes,
# hence the abundance of unnecessary comments
# all over the place

import time
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

# Constants for color. These should be the same
# as for the client
NONE = "NONE"
RED = "RED"
BLUE = "BLUE"

class ClientChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        BoxesGame: self.game = None

    def Network(self, data):
        print(f"[{self.addr}] {data}")

    def Network_requestPlace(self, data):
        print(f"[{self.addr}] {data}")

        if self.game is None:
            print("(Channel is not assigned to a game, no action taken)")
            return

        try:
            i = int(data["i"])
            j = int(data["j"])
            horizontal = bool(int(data["horizontal"]))
        except NameError as err:
            print(err)
            return
        except ValueError as err:
            print(err)
            return

        self.game.AddLine(i, j, horizontal, self)

    def to_bool(self, target) -> bool:
        if type(target) == bool:
            return target
        elif target == "True":
            return True
        elif target == "False":
            return False
        else:
            raise ValueError("Target {")

class BoxesServer(Server):
    
    # A required part of using PodSixNet
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        self.games = []

        # Calling the base class is critical here!
        Server.__init__(self, *args, **kwargs)


    def Connected(self, channel: ClientChannel, addr):
        print("New Connection: "+str(channel))

        # Add the player to a game

        if len(self.games) == 0:
            # Create a new one if none exist already
            self.NewGame(channel)

        else:
            # If one exists, we might still need 
            # to create a new one
            previousGame = self.games[len(self.games) - 1]

            # The second player is blue. If the blue
            # player exists, create a new game
            if previousGame.started:
                self.NewGame(channel)
            else:
                # Second player is blue
                previousGame.player_blue = channel
                channel.game = previousGame
                # Now that two players have joined, start the game
                previousGame.StartGame()

    def NewGame(self, first_player: ClientChannel):
        print(f"Starting game {len(self.games)}")

        # Create the game, the first player is red
        newGame = BoxesGame()
        self.games.append(newGame)
        newGame.player_red = first_player

        # Allow the client to inform the user that they are waiting for a game
        # Note that the game has not started
        newGame.player_red.Send({"action":"onJoined", "color":RED})

        # Let the player know what game to notify
        first_player.game = newGame

class BoxesGame():

    def __init__(self):
        # Whose turn is it?
        self.turn_color = RED

        # Cell colors
        self.colors = [[NONE for y in range(6)] for x in range(6)]
        
        # Horizontal and vertical line colors
        self.colors_h = [[NONE for y in range(7)] for x in range(6)]
        self.colors_v = [[NONE for y in range(6)] for x in range(7)]
        
        # Players
        self.player_red = None
        self.player_blue = None

        self.started = False

    def StartGame(self):
        self.player_blue.Send({"action":"startGame", "color":BLUE})
        self.player_red.Send({"action":"startGame", "color":RED})
        self.started = True

    def AddLine(self, i:int, j:int, horizontal:bool, player:ClientChannel):

        # There is no guarantee that the request will be valid

        # Check the player turn
        if self.turn_color == RED and player == self.player_red:
            color = RED
        
        elif self.turn_color == BLUE and player == self.player_blue:
            color = BLUE

        else:
            print(f"Unexpected request to add line: {player.addr} - ({i, j})")
            return

        # Constrain indices
        if horizontal:
            limit = 5, 6
        else:
            limit = 6, 5

        i = max(0, min(i, limit[0]))
        j = max(0, min(j, limit[1]))

        # Check for existing colors when adding
        success = False

        if horizontal and self.colors_h[i][j] == NONE:
            self.colors_h[i][j] = color
            success = True
        elif self.colors_v[i][j] == NONE:
            self.colors_v[i][j] = color
            success = True

        if success:
            message = {"action":"placeLine", "color":self.turn_color, 
                        "i":i, "j":j, "horizontal":horizontal}

            self.player_red.Send(message)
            self.player_blue.Send(message)

            if self.turn_color == RED:
                self.turn_color = BLUE
            else:
                self.turn_color = RED
        else:
            print(f"Request to overwrite line: {player.addr} - ({i, j})")

print("Starting server on localhost")
server = BoxesServer(localaddr=("localhost", 8888))

while True:
    server.Pump()
    time.sleep(0.01)
