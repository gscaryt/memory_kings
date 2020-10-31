import pygame
import logging as log
from .constants import CORNER, PAWN_SIZE, CARD_SIZE
from .pawn import Pawn
from .token import Token

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Player:
    def __init__(self, order, color):
        self.order = order
        self.color = color
        self.score = 0
        self.pawn = []
        self.token = []

    # PLACEMENT

    def place_pawn(self, board, col, row):
        self.pawn.append(Pawn(board, self.color, col, row))

    def place_tokens(self, board, col, row, col2, row2):
        self.token.append(Token(board,self.color,col,row))
        board.card[self.token[-1].position].recruited = self.color
        self.token.append(Token(board,self.color,col2,row2))
        board.card[self.token[-1].position].recruited = self.color
        self.score += 1
        log.debug(f'Player {self.color} score: {self.score}')

    # INTERFACE

    def get_pawn_screen_location(self, pawn_num):
        if self.color == 'COUNTER':
            return (
            (CORNER[0]+CARD_SIZE*(self.pawn[pawn_num].col))+(PAWN_SIZE*pawn_num)+5, 
            (CORNER[1]+CARD_SIZE*(self.pawn[pawn_num].row))-(PAWN_SIZE*(0))+5
            )
        else:
            return (
            (CORNER[0]+CARD_SIZE*(self.pawn[pawn_num].col))+(PAWN_SIZE*pawn_num)+5, 
            (CORNER[1]+CARD_SIZE*(self.pawn[pawn_num].row+1))-(PAWN_SIZE*(self.order))-5
            )