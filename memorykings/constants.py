import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CORNER = 150, 50
'''CORNER = Board upper left corner for 5x5.\n 
Can become a variable and adjust depending on 
the grid Size later.'''

WHITE = 255,255,255
DARK_GREY = 50,50,50
BLACK = 0,0,0

IMAGES_PATH = 'images/'

COLORS = ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE", "BROWN", "PINK", "DARK_GREEN"]
RANKS = ["BISHOP", "ROOK", "KNIGHT", "QUEEN"]
BACKS = ["BLACK", "WHITE"]

GRID = 5, 5 # SHOULD BECOME VARIABLE LATER

CARD_SIZE = 100
CARD_BORDER = 5
TOKEN_SIZE = 20
PAWN_SIZE = 20