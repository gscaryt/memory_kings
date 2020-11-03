import pygame
from .constants import PAWN_SIZE, CARD_SIZE, CORNER

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
log.disable(log.CRITICAL)


### PLAYERS ###

class Player:
    array = []
    recruited = None
    def __init__(self, order, color):
        self.order = order
        self.color = color
        self.score = 0
        self.pawn = []
        self.token = []
        Player.array.append(self)

    def place_pawn(self, board, col, row):
        self.pawn.append(Pawn(board, self.color, col, row))

    def place_tokens(self, board, col, row, col2, row2):
        self.token.append(Token(board,self.color,col,row))
        self.token.append(Token(board,self.color,col2,row2))
        self.score += 1
        log.debug(f'Player {self.color} score: {self.score}')

    def recruit(self, board, card_array):
        if self.pawn[0].position != self.pawn[1].position:
            if (
                card_array[self.pawn[0].position].color == card_array[self.pawn[1].position].color
                and card_array[self.pawn[0].position].rank == card_array[self.pawn[1].position].rank
                ):
                if card_array[self.pawn[0].position].is_token(Token.array) != None:
                    log.debug(f"recruit() - These cards were already recruited"
                    f" by Player {card_array[self.pawn[0].position].is_token(Token.array)}")
                    Player.recruited = None
                else:
                    self.place_tokens(board, self.pawn[0].col, self.pawn[0].row, self.pawn[1].col, self.pawn[1].row)
                    Player.recruited = self.order
        else:
            log.debug(f'recruit() - Pawns are in the same card.')
            Player.recruited = None

class CounterKing(Player):

    def place_pawn(self):
        self.pawn.append(Counter())

    def recruit(self, board, card_array):
        counter = self.array[0].pawn[0]
        counter_card = card_array[counter.position]
        for pawn in self.array[1].pawn:
            player_card = card_array[pawn.position]
            if (counter_card.is_token(Token.array) == None 
                and counter.position != pawn.position
                and counter_card.color == player_card.color
                and counter_card.rank == player_card.rank):
                Player.array[0].place_tokens(board, counter.col, counter.row, pawn.col, pawn.row)
                log.debug('counter_recruit() - The counter recruited one pair.')
                Player.recruited = self.order
                break
            else:
                Player.recruited = None


### PAWNS ###
    
class Pawn:
    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'pawn_' + self.color + '.png'
        self.position = self.row*board.cols+self.col

    def move(self, board, card_array, col, row):
        if self.move_check(card_array, col, row):
            self.record_position()
            self.col = col
            self.row = row
            self.position = row*board.cols+col
            print(f'move() - The Pawn Moved: New Coordinates: {self.col, self.row}'
                f' New Position: {self.position}')
            return True
        else:
            return False

    def move_check(self, card_array, col, row):
        '''Check the validity of a move:\n
        card_array = array with all the cards in the board\n
        col = destination column\n
        row = destination row'''
        if (col, row) == (self.col, self.row):
            '''Move to Same Location Attempt'''
            log.debug("move_check() - Move to Same Location attempt.")
            return False

        elif ((col, row) == (self.col+1, self.row) 
            or (col, row) == (self.col-1, self.row) 
            or (col, row) == (self.col, self.row+1) 
            or (col, row) == (self.col, self.row-1)
            ):
            '''Move as a Pawn (1 Orthogonal)'''
            log.debug("move_check() - Standard Pawn Move.")
            return True

        elif card_array[self.position].escort_check(self, Token.array, col, row):
            '''Calls escort_check method from the specific Card type.'''
            return True

        else:
            return False

    def record_position(self):
        self.previous = self.position

    def get_screen_location(self, pawn_num, player_order):
        return (
        (CORNER[0]+CARD_SIZE*(self.col))+(PAWN_SIZE*pawn_num)+5, 
        (CORNER[1]+CARD_SIZE*(self.row+1))-(PAWN_SIZE*(player_order))-5
        )

class Counter(Pawn):
    def __init__(self):
        self.color = "COUNTER"
        self.col = 0
        self.row = 0
        self.image = 'pawn_counter.png'
        self.position = 0

    def move(self, board):
        self.record_position()
        if self.row % 2 == 0 and not self.col == board.cols-1:
            self.col = self.col+1
        elif self.row % 2 != 0 and not self.col == 0:
            self.col = self.col-1
        else:
            self.row = self.row+1
        self.position = self.row*board.cols+self.col

    def get_screen_location(self, pawn_num, player_order):
        return (CORNER[0]+CARD_SIZE*(self.col))+5, (CORNER[1]+CARD_SIZE*(self.row))+5


### TOKENS ###

class Token:
    array = []
    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'token_' + color + '.png'
        self.position = self.row*board.cols+self.col
        Token.array.append(self)