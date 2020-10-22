from constants import Color

class BoxesGame():

    def __init__(self):
        # Whose turn is it?
        self.turn_color = Color.RED

        # Cell colors
        self.colors = [[Color.NONE for y in range(6)] for x in range(6)]
        
        # Horizontal and vertical line colors
        self.colors_h = [[Color.NONE for y in range(7)] for x in range(6)]
        self.colors_v = [[Color.NONE for y in range(6)] for x in range(7)]
        self.colors_square = [[Color.NONE for y in range(6)] for x in range(6)]
        
        # Players
        self.player_red = None
        self.player_blue = None

        # Scores
        self.score_red = 0
        self.score_blue = 0

        self.started = False

    def StartGame(self):
        self.player_blue.Send({"action":"startGame", "color":Color.BLUE})
        self.player_red.Send({"action":"startGame", "color":Color.RED})
        self.started = True

    def AddLine(self, i:int, j:int, horizontal:bool, player):

        # There is no guarantee that the request will be valid

        # Check the player turn
        if self.turn_color == Color.RED and player == self.player_red:
            color = Color.RED
        
        elif self.turn_color == Color.BLUE and player == self.player_blue:
            color = Color.BLUE

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

        if horizontal and self.colors_h[i][j] == Color.NONE:
            self.colors_h[i][j] = color
            success = True
        elif self.colors_v[i][j] == Color.NONE:
            self.colors_v[i][j] = color
            success = True

        if success:
            message = {"action":"placeLine", "color":self.turn_color, 
                        "i":i, "j":j, "horizontal":horizontal}

            self.player_red.Send(message)
            self.player_blue.Send(message)

            if self.turn_color == Color.RED:
                self.turn_color = Color.BLUE
            else:
                self.turn_color = Color.RED

            self.check_tiles(i, j, horizontal, color)
        else:
            print(f"Request to overwrite line: {player.addr} - ({i, j})")

    def check_tiles(self, i: int, j: int, horizontal: bool, color):

        # Each line affects up to two tiles
        
        to_check = []

        if horizontal:
            if j > 0:
                to_check.append((i, j - 1))
            if j < 6:
                to_check.append((i, j))
        else:
            if i > 0:
                to_check.append((i - 1, j))
            if i < 6:
                to_check.append((i, j))

        for i,j in to_check:
            
            # Only look for new changes in tiles
            if self.colors_square[i][j] == Color.NONE:
               
                # Each of the four sides should be active
                a = self.colors_h[i][j] != Color.NONE
                b = self.colors_h[i][j + 1] != Color.NONE
                c = self.colors_v[i][j] != Color.NONE
                d = self.colors_v[i + 1][j] != Color.NONE
               
                if a and b and c and d:
                    # Update tiles
                    self.colors_square[i][j] = color
                    
                    # Update score
                    if color == Color.RED:
                        self.score_red += 1
                    else:
                        self.score_blue += 1
                    
                    # Notify players of changes
                    tile_message = {"action":"placeTile", "i":i, "j":j, "color":color}
                    self.player_red.Send(tile_message)
                    self.player_blue.Send(tile_message)

                    self.player_red.Send({"action":"updateScore", 
                        "localScore":self.score_red, "remoteScore":self.score_blue})

                    self.player_blue.Send({"action":"updateScore", 
                        "localScore":self.score_blue, "remoteScore":self.score_red})




        