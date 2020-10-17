import pygame
from PodSixNet.Connection import connection

import resources, config
from constants import Color

class Game():
    
    def __init__(self):
        resources.load()
        self.init_mouse()
        self.reset(Color.NONE)
        
    def init_mouse(self):
        # Data specifying which line (if any)
        # is currently under the mouse
        self.hover_h = False
        self.hover_v = False
        self.hover_i = 0
        self.hover_j = 0

    def reset(self, local_color):
        # A local copy of the score. This does not affect the
        # actual score of the game, which is stored server-side
        self.local_score = 0
        self.remote_score = 0

        # Colors (for score display purposes only,
        # the actual logic regarding color is handled server-side)
        self.local_color = local_color

        # The server will assign a turn to us when the time is right
        self.has_turn = False

        # A local copy of the board. This does not affect the
        # actual the state of the game, which is stored server side
        self.colors_h = [[Color.NONE for y in range(7)] for x in range(6)]
        self.colors_v = [[Color.NONE for y in range(6)] for x in range(7)]

        # Red gets the first turn
        self.has_turn = self.local_color == Color.RED

    def place_line(self, i: int, j: int, 
                horizontal: bool, color):
        
        # This method is called by the Client
        # when the server informs it that a new
        # line has been placed

        if horizontal:
            self.colors_h[i][j] = color
        else:
            self.colors_v[i][j] = color

        # Update the current turn also - 
        # if the line just placed was out color
        # it is no longer out turn
        if color == self.local_color:
            self.has_turn = False
        else:
            self.has_turn = True

    def update(self, mouse_up: bool):
        # Drawing is handled in the "draw" method.
        # It remains to handle input:
        self.update_hover()
        self.check_mouseclick(mouse_up)

    def update_hover(self):
        # Clear hover from last iteration
        self.hover_h = False
        self.hover_v = False

        # Only allow hover (and thus placing) 
        # if it is our turn.
        if not self.has_turn:
            return

        # Get and convert mouse coords to coords local
        # to the board
        x, y = pygame.mouse.get_pos()
        x = x - resources.margin
        y = y - resources.margin

        # Current cell index
        self.hover_i = int(x/resources.L)
        self.hover_j = int(y/resources.L)

        # Coordinate local to current cell
        local_x = (x % resources.L) / resources.L
        local_y = (y % resources.L) / resources.L

        # What region of the cell are we in?
        #  a | b
        #  1 | 1   ...  bottom (h) (y:+1)
        #  1 | 0   ...  right (v) (x:+1)
        #  0 | 1   ...  left (v)
        #  0 | 0   ...  top (h)

        a = local_y < local_x
        b = local_y < 1 - local_x

        if a and b:
            self.hover_h = True
        elif a:
            self.hover_i += 1
            self.hover_v = True
        elif b:
            self.hover_v = True
        else:
            self.hover_j += 1
            self.hover_h = True

        # Constrain indices

        if self.hover_h:
            limit = 5, 6
        else:
            limit = 6, 5

        self.hover_i = max(0, min(self.hover_i, limit[0]))
        self.hover_j = max(0, min(self.hover_j, limit[1]))
    
    def check_mouseclick(self, mouse_up: bool):
        if not mouse_up:
            return

        target = None

        if self.hover_h:
            target = self.colors_h
        
        elif self.hover_v:
            target = self.colors_v

        if target is not None:
            if target[self.hover_i][self.hover_j] == Color.NONE:
                connection.Send({
                    "action": "requestPlace", 
                    "i": self.hover_i,
                    "j": self.hover_j,
                    "horizontal": self.hover_h
                    })

    def draw(self, screen):
        self.draw_board(screen)
        self.draw_hud(screen)

    def draw_board(self, screen):

        # Is there a way to set aliases for variables?
        L = resources.L
        W = resources.W
        margin = resources.margin
        dot_offset = resources.dot_offset

        # Horizontal lines first. 
        
        for i in range(6):
            for j in range(7):
                
                # 64 pixels per segment, plus the gap of 4 pixels

                state = self.colors_h[i][j]
                
                # Show a hover if it is possible to place there
                if state == resources.NONE and self.hover_h:
                    if self.hover_i == i and self.hover_j == j:
                        state = resources.HOVER
                
                image = resources.image_h[state]

                # Note the extra gap in the x-coord - this is for
                # the width of the first vertical line
                x = margin + (i * L) + W
                y = margin + (j * L)
                screen.blit(image, [x, y])

        # Vertical lines next. 

        for i in range(7):
            for j in range(6):

                state = self.colors_v[i][j]
                
                if state == resources.NONE and self.hover_v:
                    if self.hover_i == i and self.hover_j == j:
                        state = resources.NONE
                
                image = resources.image_v[state]

                # The extra gap is now in the y-coord
                x = margin + (i * L) 
                y = margin + (j * L) + W
                screen.blit(image, [x, y])

        # Lastly, the grid points

        for i in range(7):
            for j in range(7):
                x = margin + dot_offset + (i * L)
                y = margin + dot_offset + (j * L)
                screen.blit(resources.image_dot, [x,y])

    def draw_hud(self, screen):

        # This shouldn't ever happen in the normal course of 
        # the game, but it happens sometimes when testing
        if self.local_color == Color.NONE:
            return

        # RGB colors
        red = (255, 100, 120)
        blue = (110, 120, 255)
        white = (255, 255, 255)

        # Whose turn is it?
        if (self.local_color == Color.RED) == self.has_turn:
            text = "Red's Turn"
            color = red
        else:
            text = "Blue's Turn"
            color = blue

        margin = resources.margin
        L = resources.L

        x = margin
        y = margin * 3 + L * 6
        label = resources.font_medium.render(text, 1, color)
        screen.blit(label, [x,y])

        # The score:

        y += int(32 * config.scale)
        label = resources.font_small.render("Blue score:", 1, white)
        screen.blit(label, [x, y])

        y += int(16 * config.scale)
        label = resources.font_large.render("3", 1, blue)
        screen.blit(label, [x, y])

        x = int(360 * config.scale)
        y -= int(16 * config.scale)
        label = resources.font_small.render("Red score:", 1, white)
        screen.blit(label, [x, y])

        x = int(400 * config.scale)
        y += int(16 * config.scale)
        label = resources.font_large.render("9", 1, red)
        screen.blit(label, [x, y])
