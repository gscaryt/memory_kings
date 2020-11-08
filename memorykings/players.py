import time
from .constants import PAWN_SIZE, CARD_SIZE, CARD_BORDER, CORNER
from .pawns import Pawn, Counter
from .tokens import Token

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
        self.pawn.append(Pawn(board, self.color, len(self.pawn), col, row))

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
                    # These cards were already recruited
                    Player.who_recruited = None
                else:
                    self.place_token(board, self.pawn[0].col, self.pawn[0].row)
                    self.place_token(board, self.pawn[1].col, self.pawn[1].row)
                    self.score += 1
                    Player.who_recruited = self.order
        else:
            # Pawns are in the same card.
            Player.who_recruited = None


class CounterKing(Player):
    def place_pawn(self, board, col, row):
        """Places the Counter Pawn."""
        self.pawn.append(Counter(board, self.color, len(self.pawn), col, row))

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
                Player.who_recruited = self.order
                break
            else:
                Player.who_recruited = None


