import pygame, random
import logging as log
from .card import Card
from .constants import ALL_CARDS, CORNER, CARD_SIZE

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Board:
    def __init__(self, cols, rows):
        self.card = []
        self.cols = cols
        self.rows = rows
        self.width = cols*CARD_SIZE
        self.height = rows*CARD_SIZE

    def gen_grid(self):
        self.deck = ALL_CARDS[: self.rows*self.cols]
        random.shuffle(self.deck)
        for i in range(len(self.deck)):
            t = self.deck[i][0]
            if t == "b":
                color = "Blue"
            elif t == "y":
                color = "Yellow"
            elif t == "r":
                color = "Red"
            elif t == "g":
                color = "Green"
            elif t == "p":
                color = "Purple"
            elif t == "m":
                color = "Brown"
            else:
                color = ""
            t = self.deck[i][1]
            if t == "R":
                rank = "Rook"
            elif t == "B":
                rank = "Bishop"
            elif t == "K":
                rank = "Knight"
            elif t == "Q":
                rank = "Queen"
            t = self.deck[i][2]
            if t == "W":
                back = "White"
            else:
                back = "Black"
            self.card.append(Card(self.cols, i, color, rank, back))
            log.debug(f'gen_grid() - Card Created: {i} {self.card[i].color} {self.card[i].rank}')
        log.debug(f'gen_grid() - Cards Array: {self.card}')