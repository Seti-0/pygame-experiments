# This is a learning project, and so has way more
# comments than necessary

import pygame
from PodSixNet.Connection import connection

import config, resources
from client import Client
from game import Game
from status import StatusScreen

###########
## Setup ##
###########

# Quick note: one of pylint's jobs is to make
# sure that any functions/variables you reference actually
# exist. However, it does not by default scan C based libraries 
# like pygame. Hence there will be occasional "disable=no-member"
# comments to supress incorrect warnings.

# Initialize pygame
pygame.init() # pylint: disable=no-member

# Load user configuration (or supply defaults)
config.load()
# Load images and fonts 
resources.load()

# Create the window
width = int(432*config.scale)
height = int(530*config.scale)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Boxes")

# This object helps with loop timing
clock = pygame.time.Clock()

# "Game" is a class that keeps a local image
# of the state of the game, and can draw it, and can respond
# to user input
game = Game()

# "Client" listens to the server and will notify
# the game that changes have occurred
client = Client(game)

# "StatusSreen" is a class that knows how to draw
# the client's current status, if the client is not
# in game.
status_screen = StatusScreen(client)

# These variables will be used to keep track 
# of mouse events
mouse_up = False
mouse_up_lock = False

# A function for looking through pygame events
def check_events():
    global mouse_up, mouse_up_lock

    mouse_up_recieved = False
    for event in pygame.event.get():
    
        # This fires if the quit button is pressed
        if event.type == pygame.QUIT: # pylint: disable=no-member
            exit(0)

        if event.type == pygame.MOUSEBUTTONUP: # pylint: disable=no-member
            mouse_up_recieved = True
    
    # This is an attempt to m
    # ake sure that 
    # a mouse up event only occurs once per mouse-up
    if mouse_up_recieved: 
        mouse_up = not mouse_up_lock
        mouse_up_lock = True
    else:
        mouse_up = False
        mouse_up_lock = False   

###############
## Main Loop ##
###############

while True:

    # Update networking
    connection.Pump()
    client.Pump()

    # Check for pygame events since the last 
    # frame
    check_events()

    # Prepare the pygame screen for drawing
    # (Clear it, fill it with black)
    screen.fill(0)

    # The program has two main states - 
    # "in game", and a "status_screen" to convey messages
    # to the player outside of the game
    if client.state == client.IN_GAME:
        # Update the game, draw it
        game.update(mouse_up)
        game.draw(screen)
    else:
        # Display the current client status
        status_screen.draw(screen)

    # Replace the previous frame onscreen with the
    # new one just drawn.
    pygame.display.flip()

    # This will wait a little, with the aim
    # of having this loop execute 60 times per second
    # (and no faster!)
    clock.tick(60)