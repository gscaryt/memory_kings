import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CORNER = 150, 50 # For 5x5. Can become a variable and adjust depending on the Deck Size later.

DARK_GREY = 50,50,50
WHITE = 255,255,255
BLACK = 0,0,0

IMAGES_PATH = 'images/'

CARD_SIZE = 100
TOKEN_SIZE = 20
PAWN_SIZE = 20

ALL_CARDS = [
    "QQQ",
    "rBB","rRB","rKB","bBB","bRB","bKB",
    "rBW","rRW","rKW","bBW","bRW","bKW",
    "yBB","yRB","yKB","gBB","gRB","gKB",
    "yBW","yRW","yKW","gBW","gRW","gKW",
    # EXTRA CARDS
    "pBB","pRB","pKB","pBW","pRW","pKW",
    "mBB","mRB","mKB","mBW","mRW","mKW",
    ]