from PodSixNet.Server import Server
from channel import ClientChannel

from game import BoxesGame
from constants import Color

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
            self.new_game(channel)

        else:
            # If one exists, we might still need 
            # to create a new one
            previousGame = self.games[len(self.games) - 1]

            # The second player is blue. If the blue
            # player exists, create a new game
            if previousGame.started:
                self.new_game(channel)
            else:
                # Second player is blue
                previousGame.player_blue = channel
                channel.game = previousGame
                # Now that two players have joined, start the game
                previousGame.StartGame()

    def new_game(self, first_player: ClientChannel):
        print(f"Starting game {len(self.games)}")

        # Create the game, the first player is red
        newGame = BoxesGame()
        self.games.append(newGame)
        newGame.player_red = first_player

        # Allow the client to inform the user that they are waiting for a game
        # Note that the game has not started
        newGame.player_red.Send({"action":"onJoined", "color":Color.RED})

        # Let the player know what game to notify
        first_player.game = newGame