import pygame
import logging as log
from .player import Player
from .board import Board

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Game:
    def __init__(self):
        self.selected = False
        self.counter_turns = 0
        self.round_number = 0
        self.who_recruited = None
        self.player = []

    def setup(self, cols, rows):
        self.board = Board(cols, rows)
        self.board.gen_grid()

    def create_players(self, num_of_players):
        self.player.append(Player('COUNTER', 0))
        log.debug(f'create_players() - Player COUNTER created.')
        for i in range(num_of_players):
            self.player.append(Player(self.color_order[i], i+1))
            log.debug(f'create_players() - Player {self.color_order[i]} created.')
        log.debug(f'create_players() - Players Array: {self.player}')

    def choose_colors(self, color1, color2=None, color3=None, color4=None):
        self.color_order = (color1, color2, color3, color4)
        self.turn = 1
        log.debug(f'choose_colors() - Chosen Colors: {self.color_order}')

    def move_check(self, col, row):
        pass

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