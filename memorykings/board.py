import pygame
import random
import time
from .constants import COLORS, RANKS, BACKS, CARD_SIZE, CORNER

import logging as log
log.basicConfig(
    level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)
log.disable(log.CRITICAL)

"""
This module contains:
BOARD: Board()
CARDS: Card(), Bishop(Card), Rook(Card), Knight(Card), and Queen(Card)
"""

# BOARD

class Board:
    def __init__(self, cols, rows=None):
        self.cols = cols
        self.rows = rows if rows is not None else cols
        self.width = self.cols * CARD_SIZE
        self.height = self.rows * CARD_SIZE
        self.grid = []

    def gen_grid(self, game):
        """
        Generates all the Cards that are appended to the
        deck array, shuffles the cards, attributes their
        position and coordinates and forms a grid array
        based on the setup variant option.

        Note: Dependency of how many colors based on the board
        size is (cols*rows-special_cards)/(backs*ranks)
        """

        COLOR_NUMBER = int(
            (self.cols * self.rows - 1 + (self.cols * self.rows + 1) % 2) / 6
        )

        # GENERATE SPECIAL CARDS OUTSIDE THE LOOP
        Queen("", "QUEEN", "BLACK")

        # GENERATE CARD_TYPE BASED ON THEIR RANK
        for _, back in enumerate(BACKS):
            for _, color in enumerate(COLORS[:COLOR_NUMBER]):
                for _, rank in enumerate(RANKS):
                    if rank == "BISHOP":
                        Bishop(color, rank, back)
                    elif rank == "ROOK":
                        Rook(color, rank, back)
                    elif rank == "KNIGHT":
                        Knight(color, rank, back)
        # SHUFFLE AND ADD ATTRIBUTES TO EACH CARD
        random.shuffle(Card.deck)
        if game.setup_variant == 'alternate':
            self.gen_alternate_setup()
        else:
            self.gen_standard_setup()

    def get_card(self, col, row):
        """
        Uses the grid array to get a Card instance.
        Maybe can replace the need for "relative position".
        """
        return self.grid[row][col]

    def click_to_grid(self):
        """
        Converts the pixel coordinates of a mouse click
        to card coordinates in the grid and returns them.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        click_pos = [0, 0]
        if click[0] == 1:
            if not (
                mouse[0] < CORNER[0] or
                mouse[1] < CORNER[1] or
                mouse[0] > CORNER[0] + self.rows * CARD_SIZE or
                mouse[1] > CORNER[1] + self.cols * CARD_SIZE
            ):
                for i in range(self.rows):
                    if (
                        i <= (mouse[0] - CORNER[0]) / CARD_SIZE and
                        (mouse[0] - CORNER[0] - CARD_SIZE) / CARD_SIZE <= i
                    ):
                        click_pos[0] = i
                        break
                for j in range(self.cols):
                    if (
                        j <= (mouse[1] - CORNER[1]) / CARD_SIZE and
                        (mouse[1] - CORNER[1] - CARD_SIZE) / CARD_SIZE <= j
                    ):
                        click_pos[1] = j
                        break
                log.debug(
                    f"click_to_grid() - Mouse click on {mouse}"
                    f"represents the {click_pos} coordinates."
                )
                return click_pos
            else:
                log.debug(f"click_to_grid() - Mouse click outside the board.")
                return None

    def gen_standard_setup(self):
        '''Forms a standard grid with randomly placed cards.'''
        for i, card in enumerate(Card.deck):
            card.position = i
            card.col = i % self.cols
            card.row = i // self.cols
        for i in range(0, len(Card.deck), self.cols):
            grid_slice = Card.deck[i: i + self.cols]
            self.grid.append(grid_slice)

    def gen_alternate_setup(self):
        '''Forms an alternate Chess-like grid.'''
        blacks = []
        whites = []
        alternate_deck =[]
        for i, card in enumerate(Card.deck):
            if card.back == 'BLACK':
                blacks.append(card)
            elif card.back == 'WHITE':
                whites.append(card)

        b = 0
        w = 0
        for j in range(self.rows):
            for i in range(self.cols):
                if i%2 == j%2:
                    alternate_deck.append(blacks[b])
                    b += 1
                else:
                    alternate_deck.append(whites[w])
                    w += 1

        Card.deck = alternate_deck
        for i, card in enumerate(Card.deck):
            card.position = i
            card.col = i % self.cols
            card.row = i // self.cols
        for i in range(0, len(Card.deck), self.cols):
            grid_slice = Card.deck[i: i + self.cols]
            self.grid.append(grid_slice)

            
# CARDS

class Card:
    deck = []

    def __init__(self, color, rank, back):
        self.color = color
        self.rank = rank
        self.back = back
        self.image = color + "_" + rank + ".png"
        self.recruited = None
        self.position = 0
        self.col = 0
        self.row = 0
        Card.deck.append(self)

    def get_token(self, token_array):
        """
        Returns the color of a token in the same
        position as this card instance.
        """
        for token in token_array:
            if token.position == self.position:
                return token.color
        return None

    def escort_token_check(self, pawn, token_array, col, row):
        """
        Check to see if there is a token of a different player
        on the same card as the pawn trying to move and if they
        have the same color. A pawn cannot use Escort movement
        if the card has a token of an opponent.
        """
        log.debug(
            f"escort_token_check() - Is token {self.get_token(token_array)}"
            f" on {self.position}. Pawn position: {pawn.position}"
        )
        if (
            self.get_token(token_array) is not None and
            self.get_token(token_array) != pawn.color
        ):
            log.debug(
                f"escort_token_check() - There is an Opponent's Token"
                f" on Card {self.position}"
            )
            return True

    def activate(self, window, game, board, display, player_array):
        """
        Check if a card was hidden or open when a pawn moves
        to it. Special powers (like the Queen's Peeking Card) only
        activate when a card is flipped from facing down to up.
        """
        for player in player_array:
            for pawn in player.pawn:
                for token in player.token:
                    if token.position == self.position:
                        log.debug(
                            f"activate() - DON'T ACTIVATE Card {self.position}"
                        )
                        return False
                if pawn.previous == self.position:
                    log.debug(f"activate() - DON'T ACTIVATE Card {self.position}")
                    return False
        log.debug(f"activate() - ACTIVATE Card {self.position}")
        return self.special(window, game, board, display, player_array)

    def special(self, *args, **kwargs):
        """Standard Cards have no special effects."""
        pass


class Bishop(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an escort_token_check and then checks if the
        destination is on a diagonal from the card.
        """
        if not self.escort_token_check(pawn, token_array, col, row):
            if abs(col - self.col) == abs(row - self.row):
                log.debug(
                    f"escort_check() - Valid Bishop Escort."
                    f" {self.col}, {self.row} >> {col}, {row}"
                )
                return True
            else:
                log.debug(
                    f"escort_check() - The Bishop cannot Escort to {col}, {row}."
                )
                return False
        else:
            return False


class Rook(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an escort_token_check and then checks if the
        destination is on a orthogonal from the card.
        """
        if self.escort_token_check(pawn, token_array, col, row):
            return False
        else:
            if col == self.col or row == self.row:
                log.debug(
                    f"escort_check() - Valid Rook Escort."
                    f" {self.col}, {self.row} >> {col}, {row}"
                )
                return True
            else:
                log.debug(
                    f"escort_check() - The Rook cannot Escort to {col}, {row}."
                )
                return False


class Knight(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an escort_token_check and then checks if the
        destination is on an "L" pattern from the card.
        """
        if not self.escort_token_check(pawn, token_array, col, row):
            if (abs(col - self.col) == 2 and abs(row - self.row) == 1) or (
                abs(col - self.col) == 1 and abs(row - self.row) == 2
            ):
                log.debug(
                    f"escort_check() - Valid Knight Escort."
                    f" {self.col}, {self.row} >> {col}, {row}"
                )
                return True
            else:
                log.debug(
                    f"escort_check() - The Knight cannot Escort to {col}, {row}."
                )
                return False
        else:
            return False


class Queen(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an escort_token_check and then checks if the
        destination is orthogonal or diagonal from the card.
        """
        if not self.escort_token_check(pawn, token_array, col, row):
            if (abs(col - self.col) == abs(row - self.row)) or (
                (col == self.col) or (row == self.row)
            ):
                log.debug(
                    f"escort_check() - Valid Queen Escort."
                    f" {self.col}, {self.row} >> {col}, {row}"
                )
                return True
            else:
                log.debug(
                    f"escort_check() - The Queen cannot Escort to {col}, {row}."
                )
                return False
        else:
            return False

    def special(self, window, game, board, display, player_array):
        """
        When the Queen is activated, the Player can
        peek any hidden card from the board.
        """
        log.debug("special() - Queen's Advice starts running.")
        display.print_all(window, game, board, self.deck, player_array)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = board.click_to_grid()
                    if click_pos is not None:
                        if not display.print_card(
                            window,
                            board,
                            self.deck,
                            player_array,
                            click_pos[0],
                            click_pos[1],
                        ):
                            log.debug(
                                "special() - Failed to click a valid card."
                            )
                            continue
                        else:
                            log.debug("special() - Print card.")
                            return True
