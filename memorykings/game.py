import pygame
import time
from .constants import CARD_SIZE, PAWN_SIZE, CORNER, PLAYER_COLORS
from .players import Player, CounterKing
from .board import Card

import logging as log
log.basicConfig(
    level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)
log.disable(log.CRITICAL)


class Game:
    def __init__(self):
        self.creating = True
        self.num_of_players = 1
        self.grid_size = (5,5)
        self.setup_variant = 'standard'
        self.counter = None
        self.current_player = None
        self.current_turn = 1
        self.all_pawns_set = False
        self.pawn_selected = False
        self.end_turn = False

    def choose_players(self, number):
        self.num_of_players = number
        log.debug(self.num_of_players)

    def choose_grid(self):
        if self.grid_size == (5, 5):
            self.grid_size = (6, 6)
            log.debug(self.grid_size)
        else:
            self.grid_size = (5, 5)
            log.debug(self.grid_size)

    def choose_setup(self):
        if self.setup_variant == 'standard':
            self.setup_variant = 'alternate'
            log.debug(self.setup_variant)
        else:
            self.setup_variant = 'standard'
            log.debug(self.setup_variant)

    def play_game(self):
        log.debug('Start')
        self.creating = False

    def create_players(self):
        """
        1) Creates the CounterKing in the 0th Player.array
        position even if it is a multiplayer game.
        2) Creates the actual Players.
        3) Set all Game Attributes to their starting values.
        """
        counter = CounterKing(0, "COUNTER")
        log.debug(
            f"create_players() - Player {counter.order} - {counter.color} created."
        )
        log.debug(f"{Player.array}")

        for i in range(1, self.num_of_players + 1):
            player = Player(i, PLAYER_COLORS[i])
            log.debug(
                f"create_players() - Player {player.order} - {player.color} created."
            )
        log.debug(f"{Player.array}")

        self.num_of_players = len(Player.array)
        self.current_player = Player.array[self.current_turn]
        self.pawn_selected = False
        self.counter = Player.array[0]
        self.all_pawns_set = False
        self.end_turn = False

    def place_pawns(self, board, event):
        """
        If this is a Multiplayer game, skips the turn 0, so the
        Counter Pawn is not placed.

        Placement continues until the last player placed 2 pawns.
        """
        if self.num_of_players == 2 and len(self.counter.pawn) != 1:
            time.sleep(0.5)
            self.counter.place_pawn()

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = board.click_to_grid()
            self.current_player.place_pawn(
                board, click_pos[0], click_pos[1]
                )
            self.change_turn()
            if self.current_turn == 0:
                self.current_turn = 1
                self.current_player = Player.array[1]
        
        last_player = Player.array[self.num_of_players-1]
        self.all_pawns_set = bool(len(last_player.pawn) == 2)
        if self.all_pawns_set:
            self.current_turn = 1
            self.pawn_selected = False
            log.debug(
                f"place_pawns() - All pawns set: {self.all_pawns_set}"
            )

    # SELECT/MOVE

    def select(self, window, board, display):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if self.pawn_selected:
                click_pos = board.click_to_grid()
                if click_pos is not None:
                    if not self.pawn_selected.move(
                        board, Card.deck, click_pos[0], click_pos[1]
                    ):
                        log.debug(f"select() - Failed to move. Unselected.")
                        self.pawn_selected = False
                    else:
                        log.debug(f"select() - Successful move.")
                        if not Card.deck[self.pawn_selected.position].activate(
                            window, self, board, display, Player.array
                        ):
                            self.pawn_selected = False
                            self.end_turn = True
                        else:
                            self.pawn_selected = False
                            self.end_turn = True
                else:
                    log.debug(f"select() - Failed to move. Unselected.")
                    self.pawn_selected = False
            else:
                self.current_player = Player.array[self.current_turn]
                log.debug(f"select() - Current Turn: {self.current_turn}")
                for pawn_num, pawn in enumerate(self.current_player.pawn):
                    coords = pawn.get_screen_location(
                        pawn_num, self.current_turn
                    )
                    log.debug(f"select() - Pawn {pawn_num}: {coords}")
                    log.debug(
                        f"select() -"
                        f" {coords[0]-PAWN_SIZE < mouse[0] < coords[0]+PAWN_SIZE}"
                        f" and {coords[1]-PAWN_SIZE < mouse[1] < coords[1]+PAWN_SIZE}"
                        f" {mouse}"
                    )
                    if (
                        click[0] == 1 and
                        coords[0] < mouse[0] < coords[0] + PAWN_SIZE and
                        coords[1] < mouse[1] < coords[1] + PAWN_SIZE
                    ):
                        self.pawn_selected = self.current_player.pawn[pawn_num]
                        self.pawn_selected_num = pawn_num
                        self.end_turn = False
                        log.debug(
                            f"select() - Pawn Selected: {self.pawn_selected}"
                            f"is on the {Card.deck[self.pawn_selected.position]} Card"
                        )
                        break
                    else:
                        self.pawn_selected = False
                        self.end_turn = False

    # GAME FLOW

    def change_turn(self):
        """
        Increases the current turn up to the last player
        and then back to 0. Updates the current_player.
        """
        if self.current_turn < self.num_of_players - 1:
            self.current_turn += 1
        else:
            self.current_turn = 0
        if self.current_turn == 0 and self.num_of_players > 2:
            """If multiplayer, skip the CounterKing turn (0)"""
            self.current_turn = 1
        self.current_player = Player.array[self.current_turn]
        self.end_turn = False
        log.debug(f"change_turn - Next Player: {self.current_player.color}")

    def round(self, window, board, display):
        self.get_all_pawns_positions()
        if self.num_of_players == 2 and Player.who_recruited == 0:
            time.sleep(1)
            self.counter.pawn[0].move(board)
            self.recruit_check(board)
        elif self.num_of_players == 2 and self.current_turn == 0:
            self.counter.pawn[0].move(board)
            self.end_turn = True
            self.recruit_check(board)
            time.sleep(0.7)
        else:
            self.select(window, board, display)
            Player.who_recruited = None
            self.recruit_check(board)

    # CHECKS

    def get_all_pawns_positions(self):
        """
        Records all pawns current positions as previous.
        Used at the beginning of the round, to record the
        state of the board before moving so it can be
        checked if a card was just flipped or not
        """
        for player in Player.array:
            for pawn in player.pawn:
                pawn.previous = pawn.position

    def recruit_check(self, board):
        """
        Calls for Recruit Checks. On SOLO games (num_of_players == 2)
        the Counter King has priority over recruiting.
        """
        if self.num_of_players == 2:
            self.counter.recruit(board, Card.deck)
        if Player.who_recruited is None:
            self.current_player.recruit(board, Card.deck)
        if Player.who_recruited is not None:
            self.current_turn = Player.who_recruited
            self.current_player = Player.array[self.current_turn]
            self.end_turn = False

    def end_game_check(self):
        """Checks for End Game conditions"""
        try:
            if Player.array[0].pawn[0].position == len(Card.deck) - 1:
                log.debug(
                    "end_game_check() - The game is finished!"
                    "Counter on the 25 card."
                )
                return True
            elif self.num_of_players == 2:
                if Player.array[0].score == 6:
                    log.debug(
                        "end_game_check() - The game is finished!"
                        "Counter recruited 6 pairs"
                    )
                    return True
                elif Player.array[1].score == 6:
                    log.debug(
                        "end_game_check() - The game is finished!"
                        "You won with 6 pairs"
                    )
                    return True
            else:
                for player in Player.array:
                    if player.score == 12 // (self.num_of_players - 1):
                        log.debug(
                            "end_game_check() - The game is finished!"
                            "You won!"
                        )
                        return True
            return False
        except:
            pass
