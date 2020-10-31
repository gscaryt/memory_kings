import pygame
import logging as log
from .constants import CARD_SIZE, CORNER
from .player import Player
from .board import Board

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Game:
    def __init__(self):
        self.counter_turns = 0
        self.round_number = 0
        self.who_recruited = None
        self.player = []
        self.turn = 0
        self.all_pawns_set = False

    def setup(self, cols, rows):
        self.board = Board(cols, rows)
        self.board.gen_grid()

    def choose_colors(self, color1='ORANGE', color2='PURPLE', color3='BLACK', color4='WHITE'):
        self.color_order = ('COUNTER', color1, color2, color3, color4)
        log.debug(f'choose_colors() - Chosen Colors: {self.color_order}')

    def create_players(self, num_of_players):
        for i in range(num_of_players+1):
            self.player.append(Player(i, self.color_order[i]))
            log.debug(f'create_players() - Player {self.player[i].order} - {self.player[i].color} created.')

    def place_pawns(self, board):
        if self.turn == 0 and len(self.player) != 2:
            self.turn += 1
        elif self.turn == 0 and len(self.player) == 2 and len(self.player[0].pawn) == 0:
            self.player[self.turn].place_pawn(board, 0, 0)
            self.change_turn()
        elif self.turn == 0 and len(self.player) == 2 and len(self.player[0].pawn) == 1:
            self.change_turn()
        else:
            click_pos = self.click_to_grid(board)
            self.player[self.turn].place_pawn(board, click_pos[0], click_pos[1])
            self.change_turn()
        self.all_pawns_set = bool(len(self.player[len(self.player)-1].pawn) == 2)
        if self.all_pawns_set:
            self.turn = 1

    def change_turn(self):
        if self.turn != len(self.player)-1:
            self.turn += 1
        else:
            self.turn = 0
        if self.turn == 0 and len(self.player) != 2:
            self.turn = 1
        log.debug(f'change_turn - Next Player: {self.turn}')

    def counter_move(self, board):
        counter = self.player[0].pawn[0]
        if counter.row % 2 == 0 and not counter.col == board.cols-1:
            counter.move_pawn(board, counter.col+1, counter.row)
        elif counter.row % 2 != 0 and not counter.col == 0:
            counter.move_pawn(board, counter.col-1, counter.row)
        else:
            counter.move_pawn(board, counter.col, counter.row+1)
        self.change_turn()

## INTERACTION

    def click_to_grid(self, board):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        click_pos = [0, 0]
        if click[0] == 1:
            if not (mouse[0] < CORNER[0] or mouse[1] < CORNER[1] 
                or mouse[0] > CORNER[0]+board.cols*CARD_SIZE
                or mouse[1] > CORNER[1]+board.rows*CARD_SIZE):
                for i in range(self.board.cols):
                    if i < (mouse[0]-150)/CARD_SIZE and (mouse[0]-150-CARD_SIZE)/CARD_SIZE < i:
                        click_pos[0] = i
                for j in range(self.board.rows):
                    if j < (mouse[1]-50)/CARD_SIZE and (mouse[1]-50-CARD_SIZE)/CARD_SIZE < j:
                        click_pos[1] = j
                log.debug(f'click_to_grid() - Mouse click on {mouse} represents the {click_pos} coordinates.')
                return click_pos
            else:
                log.debug(f'click_to_grid() - Mouse click outside the board.')
                return None

## TODO

    def recruit_check(self):
        pass

    def queen_check(self):
        pass

    def end_game_check(self):
        pass

    def get_game_state(self):
        pass

    def player_turn(self):
        pass

    def counter_turn(self):
        pass

    def round(self):
        pass
