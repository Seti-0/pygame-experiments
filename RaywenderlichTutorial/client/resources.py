import pygame
import config
from constants import Color

# Constants for image types
NONE = Color.NONE
BLUE = Color.BLUE
RED = Color.RED
HOVER = "Hover"

loaded = False

image_h = {}
image_v = {}
image_square = {}
image_dot = None
L = W = margin = 0
font_small = font_medium = font_large = None

def load():
    global loaded
    if loaded:
        return
    loaded = True
    reload()

def reload():

    # For horizontal and vertical lines, and grid points
    global image_h, image_v, image_dot, image_square

    image_dot = pygame.image.load("images/dot.png")
    dot_length = image_dot.get_size()[0]

    image_square[BLUE] = pygame.image.load("images/square_blue.png")
    image_square[RED] = pygame.image.load("images/square_red.png")

    image_h = {}
    image_h[NONE] = pygame.image.load("images/line.png")
    image_h[HOVER] = pygame.image.load("images/line_yellow.png")
    image_h[BLUE] = pygame.image.load("images/line_blue.png")
    image_h[RED] = pygame.image.load("images/line_red.png")
    size_h = image_h[NONE].get_size()

    # We need the config "scale" value
    config.load()

    # Apply global scale
    size_h = (int(size_h[0] * config.scale), int(size_h[1] * config.scale))
    for state in [NONE, HOVER, BLUE, RED]:
        image_h[state] = pygame.transform.scale(image_h[state], size_h)
    dot_length = int(dot_length * config.scale)
    image_dot = pygame.transform.scale(image_dot, (dot_length, dot_length))

    # The vertical lines are just the horizontal lines
    # rotated
    image_v = {}
    for state in [NONE, HOVER, BLUE, RED]:
        image_v[state] = pygame.transform.rotate(image_h[state], -90)

    # Some hints for drawing
    global L, W, dot_offset, margin

    # Cell length and grid length
    L = size_h[0] + size_h[1]
    W = size_h[1]

    # The dot is a little larger than the actual grid point
    dot_offset = int((size_h[1] - dot_length) / 2)

    # A general constant for margins
    margin = int(10 * config.scale)

    # Fonts. Large is used for score numbers.
    # Medium is used for the turn indicator, small is used to label
    # the scores.

    global font_small, font_medium, font_large

    medium = int(32 * config.scale)
    small = int(16 * config.scale)
    large = int(64 * config.scale)
    font_medium = pygame.font.SysFont(None, medium)
    font_small = pygame.font.SysFont(None, small)
    font_large = pygame.font.SysFont(None, large)
