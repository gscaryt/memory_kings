import pygame
from .constants import PLAYER_COLORS
from .players import Player, CounterKing
from .board import Board
from .cards import Card

class Game:
    def __init__(self):
        self._init()

    def _init(self):
        self._creating = True
        self._grid_size = (5, 5)
        self._setup_variant = "standard"
        self._all_pawns_set = False
        self._num_of_players = 2
        self._winner = None
        self._abandoned = False
        self._turns = 0

        self.board = None
        self.ongoing_turn = 1
        self.end_turn = False
    
    def _reset(self):
        self._init()
        Player.array = []
        Card.array = []

    @property
    def counter(self):
        return Player.array[0]

    @property
    def current(self):
        return Player.array[self.ongoing_turn]

    # CREATING THE GAME

    def choose_players(self, number):
        self._num_of_players = number + 1

    def choose_grid(self):
        if self._grid_size == (5, 5):
            self._grid_size = (6, 6)
        else:
            self._grid_size = (5, 5)

    def choose_setup(self):
        if self._setup_variant == "standard":
            self._setup_variant = "alternate"
        else:
            self._setup_variant = "standard"

    def play_game(self):
        self._creating = False

    def create_board(self):
        """Creates the board with the chosen grid size and setup variant"""
        self.board = Board(self._grid_size[0], self._grid_size[1])
        self.board.gen_deck()
        self.board.gen_grid(self._setup_variant)
        del self._grid_size
        del self._setup_variant

    def create_players(self):
        """
        1) Creates the CounterKing in the 0th Player.array
        position even if it is a multiplayer game.
        2) Creates the actual Players.
        3) Set all Game Attributes to their starting values.
        """
        counter = CounterKing(0, "COUNTER")

        for i in range(1, self._num_of_players):
            player = Player(i, PLAYER_COLORS[i])
        
        Player.total = self._num_of_players
        del self._num_of_players

    # PAWNS' SETUP

    def place_pawns(self, display, event):
        """
        If this is a Multiplayer game, skips the turn 0, so the
        Counter Pawn is not placed.

        Placement continues until the last player placed 2 pawns.
        """
        if Player.total == 2 and len(self.counter.pawn) != 1:
            self.counter.place_pawn(0,0)
            pygame.time.wait(800)

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = self.board.get_click_to_pos(display)
            if position is None:
                return
            if not self.place_pawns_check(position[0], position[1]):
                return
            else:
                self.current.place_pawn(position[0], position[1])
                self.change_turn()
                if self.ongoing_turn == 0:
                    self.ongoing_turn = 1

        last_player = Player.array[Player.total-1]
        self._all_pawns_set = bool(len(last_player.pawn) == 2)
        if self._all_pawns_set:
            self.ongoing_turn = 1
        
    def place_pawns_check(self, col, row):
        """
        Checks if the coordinates are a valid position for
        placing a pawn during setup.
        - Solo: Must start on cards with same Back as Counter.
        - Multiplayer: Must start on White Backs.
        row: Row to place the pawn.
        col: Column to place the pawn.
        """
        card = self.board.get_card(col, row)
        if Player.total == 2:
            counter = self.counter.pawn[0]
            card_counter = self.board.get_card(counter.col, counter.row)
            if card.back == card_counter.back:
                return True
        elif Player.total > 2 and card.back == "WHITE":
            return True
        else:
            return False

    # GAME FLOW

    def change_turn(self):
        """
        Increases the current turn up to the last player
        and then back to 0. Updates the current_player.
        """
        if self.ongoing_turn < Player.total - 1:
            self.ongoing_turn += 1
        else:
            self.ongoing_turn = 0
        if self.ongoing_turn == 0 and Player.total > 2:
            # If multiplayer, skip the CounterKing turn (0)
            self.ongoing_turn = 1
        self.end_turn = False

    def round(self, display):
        Player._get_all_pawns_positions()

        if Player.total == 2 and self.ongoing_turn == 0:
            self.counter.pawn[0]._move(self.board)
            self.end_turn = True
            pygame.time.wait(600)

        else:
            if self.current.turn(display, self.board):
                self.end_turn = True

            if Player.total == 2 and self.counter.recruit(self.board) == 0:
                self.counter.pawn[0]._move(self.board)
                pygame.time.wait(600)

        self.recruit_check()

    def recruit_check(self):
        """
        Calls for Recruit Checks. On SOLO games (num_of_players == 2)
        the Counter King has priority over recruiting.
        """
        recruited = None
        if Player.total == 2:
            recruited = self.counter.recruit(self.board)
        if recruited is None:
            recruited = self.current.recruit(self.board)
        if recruited is not None:
            self.ongoing_turn = recruited
            self.end_turn = False

    def is_end_game(self):
        """Checks for End Game conditions"""
        if Player.total == 2:
            try:
                if (
                    self.counter.pawn[0].position
                    == (self.board.cols-1, self.board.rows-1)
                ):
                    # Player Loses
                    self._winner = self.counter
                    return True
            except IndexError:
                pass
            if self.counter.score == 6:
                # Player Loses
                self._winner = self.counter
                return True
            elif Player.array[1].score == 6:
                # Player Wins
                self._winner = Player.array[1]
                return True
        else:
            for player in Player.array:
                if player.score == 12 // (Player.total - 1):
                    # That Player Wins
                    self._winner = player
                    return True
        return False
