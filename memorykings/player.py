import pygame
import logging as log
from .pawn import Pawn
from .token import Token
from .constants import CORNER, PAWN_SIZE, CARD_SIZE

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
log.disable(log.CRITICAL)

class Player:
    def __init__(self, color, num):
        self.color = color
        self.num = num
        self.score = 0
        self.pawn = []
        self.token = []

    def place_pawn(self, col, row, board_cols):
        self.pawn.append(Pawn(self.color, col, row, board_cols))

    def place_tokens(self, col, row, col2, row2, board_cols):
        self.token.append(Token(self.color,col,row,board_cols))
        self.token.append(Token(self.color,col2,row2,board_cols))
        self.score += 1
    
    def counter_move(self, board_cols):
        counter = self.pawn[0] # Counter King has only pawn[0] of player[0].
        if counter.row % 2 != 0 and not counter.col == board_cols:
            counter.col += 1
        elif counter.row % 2 == 0 and not counter.col == 0:
            counter.col -= 1
        else:
            counter.row += 1

    def move(self, col, row):
        if move_check(self.selected, col, row):
            self.pawn[self.selected].move(col, row)
        else:
            self.selected = None

    def move_check(self, col, row):
        pass

    # SCREEN INTERACTION

    def get_pawn_location(self, pawn_num):
        if self.color == 'COUNTER':
            return (
            (CORNER[0]+CARD_SIZE*(self.pawn[pawn_num].col))+(PAWN_SIZE*pawn_num)+5, 
            (CORNER[1]+CARD_SIZE*(self.pawn[pawn_num].row))-(PAWN_SIZE*(0))+5
            )
        else:
            return (
            (CORNER[0]+CARD_SIZE*(self.pawn[pawn_num].col))+(PAWN_SIZE*pawn_num)+5, 
            (CORNER[1]+CARD_SIZE*(self.pawn[pawn_num].row+1))-(PAWN_SIZE*(self.num))-5
            )

    def select_pawn(self, turn):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if turn == self.num:
            for pawn_num in range(len(self.pawn)):
                coords = self.get_pawn_location(pawn_num)
                log.debug(
                    f'select_pawn() - {click[0] == 1}'
                    f' {coords[0]-PAWN_SIZE < mouse[0] < coords[0]+PAWN_SIZE}'
                    f' and {coords[1]-PAWN_SIZE < mouse[1] < coords[1]+PAWN_SIZE}'
                    )
                if (click[0] == 1 
                    and coords[0] < mouse[0] < coords[0]+PAWN_SIZE
                    and coords[1] < mouse[1] < coords[1]+PAWN_SIZE
                ):
                    self.selected = pawn_num
                    log.debug(f'select_pawn() - Pawn Selected: {self.selected}')
                    