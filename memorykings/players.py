import time
from .constants import PAWN_SIZE, CARD_SIZE, CARD_BORDER, CORNER

import logging as log
log.basicConfig(
    level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)
log.disable(log.CRITICAL)

"""
This module contains:
PLAYERS: Player() and CounterKing(Player)
PAWNS: Pawn() and Counter(Pawn)
TOKENS: Token()
"""

# PLAYERS


class Player:
    array = []
    who_recruited = None

    def __init__(self, order, color):
        self.order = order
        self.color = color
        self.score = 0
        self.pawn = []
        self.token = []
        Player.array.append(self)

    def place_pawn(self, board, col, row):
        """Places one Pawn on the col, row of the board."""
        self.pawn.append(Pawn(board, self.color, col, row))

    def place_token(self, board, col, row):
        """Places one Token on the col, row of the board."""
        self.token.append(Token(board, self.color, col, row))

    def recruit(self, board, card_array):
        """
        Checks if both pawns of a Player are on different
        cards of the same rank and color. If so:
        1) calls place_token() on the coordinates of both pawns
        2) increases the Player score
        3) set Player.who_recruited to that Player.order number
        """
        card_0 = card_array[self.pawn[0].position]
        card_1 = card_array[self.pawn[1].position]
        if self.pawn[0].position != self.pawn[1].position:
            if card_0.color == card_1.color and card_0.rank == card_1.rank:

                if card_0.get_token(Token.array) is not None:
                    log.debug(
                        f"recruit() - These cards were already"
                        f" recruited by Player {card_0.get_token(Token.array)}"
                    )
                    Player.who_recruited = None
                else:
                    self.place_token(board, self.pawn[0].col, self.pawn[0].row)
                    self.place_token(board, self.pawn[1].col, self.pawn[1].row)
                    self.score += 1
                    Player.who_recruited = self.order
        else:
            log.debug(f"recruit() - Pawns are in the same card.")
            Player.who_recruited = None


class CounterKing(Player):
    def place_pawn(self):
        """Places the Counter Pawn."""
        self.pawn.append(Counter())

    def recruit(self, board, card_array):
        """
        Checks if the Counter Pawn is on a card of the
        same rank and color of one of the Player's. If so:
        1) calls place_token() on the coordinates of both pawns
        2) increases the Counter score
        3) set Player.who_recruited to Counter order number
        """
        counter = Player.array[0].pawn[0]
        counter_card = card_array[counter.position]
        for pawn in self.array[1].pawn:
            player_card = card_array[pawn.position]
            if (
                counter_card.get_token(Token.array) is None and
                counter.position != pawn.position and
                counter_card.color == player_card.color and
                counter_card.rank == player_card.rank
            ):
                self.place_token(board, counter.col, counter.row)
                self.place_token(board, pawn.col, pawn.row)
                self.score += 1
                log.debug(
                    "counter_recruit() - The counter recruited one pair."
                )
                Player.who_recruited = self.order
                break
            else:
                Player.who_recruited = None


# PAWNS


class Pawn:
    array = []

    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = "pawn_" + self.color + ".png"
        self.position = self.row * board.cols + self.col
        self.previous = self.position
        Pawn.array.append(self)

    def move(self, board, card_array, col, row):
        """
        1) Calls move_check()
        2) if True, changes Pawn coordinates and position
        3) returns True or False
        """
        if self.move_check(card_array, col, row):
            self.col = col
            self.row = row
            self.position = row * board.cols + col
            log.debug(
                f"move() - The Pawn Moved: New Coordinates: "
                f"{self.col, self.row} New Position: {self.position}"
            )
            return True
        else:
            return False

    def move_check(self, card_array, col, row):
        """
        Checks for the validity of a move.
        Returns True or False.
        """
        if (col, row) == (self.col, self.row):
            """Move to Same Location Attempt"""
            log.debug("move_check() - Move to Same Location attempt.")
            return False
        elif (
            (col, row) == (self.col + 1, self.row) or
            (col, row) == (self.col - 1, self.row) or
            (col, row) == (self.col, self.row + 1) or
            (col, row) == (self.col, self.row - 1)
        ):
            """Move as a Pawn (1 Orthogonal)"""
            log.debug("move_check() - Standard Pawn Move.")
            return True
        elif card_array[self.position].escort_check(
            self, Token.array, col, row
        ):
            """Calls escort_check method from the specific Card type."""
            return True
        else:
            return False

    def get_screen_location(self, pawn_num, player_order):
        """
        Get pixel coordinates of a pawn on the screen.
        Note: pawn_num and player_order are multiplying
        PAWN_SIZE so they don't print over each other.
        """
        return (
            (CORNER[0] + CARD_SIZE * (self.col)) +
            (PAWN_SIZE * pawn_num) +
            CARD_BORDER,
            (CORNER[1] + CARD_SIZE * (self.row + 1)) -
            (PAWN_SIZE * (player_order)) -
            CARD_BORDER,
        )


class Counter(Pawn):
    def __init__(self):
        self.color = "COUNTER"
        self.col = 0
        self.row = 0
        self.image = "pawn_counter.png"
        self.position = 0
        self.previous = 0

    def move(self, board):
        """
        Moves the Counter Pawn in a raster pattern
        from Card 0 down to Card 24
        """
        if self.row % 2 == 0 and not self.col == board.cols - 1:
            self.col = self.col + 1
        elif self.row % 2 != 0 and not self.col == 0:
            self.col = self.col - 1
        else:
            self.row = self.row + 1
        self.position = self.row * board.cols + self.col

    def get_screen_location(self, pawn_num, player_order):
        """
        Get pixel coordinates of the Counter Pawn on the
        screen (Top Left of the Cards).
        """
        return (
            (CORNER[0] + CARD_SIZE * (self.col)) + CARD_BORDER,
            (CORNER[1] + CARD_SIZE * (self.row)) + CARD_BORDER,
        )


# TOKENS


class Token:
    array = []

    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = "token_" + color + ".png"
        self.position = self.row * board.cols + self.col
        Token.array.append(self)
