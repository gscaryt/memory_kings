import pygame
import random
from .cards import Card, Bishop, Rook, Knight, Queen
from .constants import COLORS, RANKS, BACKS, CARD_SIZE, CORNER


class Board:
    def __init__(self, cols, rows=None):
        self.cols = cols
        self.rows = rows if rows is not None else cols
        self.width = self.cols * CARD_SIZE
        self.height = self.rows * CARD_SIZE
        self.grid = []

    def gen_grid(self, setup_variant):
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
        if setup_variant == "alternate":
            self.gen_alternate_setup()
        else:
            self.gen_standard_setup()

    def gen_standard_setup(self):
        """Forms a standard grid with randomly placed cards."""
        for i, card in enumerate(Card.deck):
            card.position = i
            card.col = i % self.cols
            card.row = i // self.cols
        for i in range(0, len(Card.deck), self.cols):
            grid_slice = Card.deck[i: i + self.cols]
            self.grid.append(grid_slice)

    def gen_alternate_setup(self):
        """Forms an alternate Chess-like grid."""
        blacks = []
        whites = []
        alternate_deck = []
        for i, card in enumerate(Card.deck):
            if card.back == "BLACK":
                blacks.append(card)
            elif card.back == "WHITE":
                whites.append(card)

        b = 0
        w = 0
        for j in range(self.rows):
            for i in range(self.cols):
                if i % 2 == j % 2:
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
                mouse[0] < CORNER[0]
                or mouse[1] < CORNER[1]
                or mouse[0] > CORNER[0] + self.rows * CARD_SIZE
                or mouse[1] > CORNER[1] + self.cols * CARD_SIZE
            ):
                for i in range(self.rows):
                    if (
                        i <= (mouse[0] - CORNER[0]) / CARD_SIZE
                        and (mouse[0] - CORNER[0] - CARD_SIZE) / CARD_SIZE <= i
                    ):
                        click_pos[0] = i
                        break
                for j in range(self.cols):
                    if (
                        j <= (mouse[1] - CORNER[1]) / CARD_SIZE
                        and (mouse[1] - CORNER[1] - CARD_SIZE) / CARD_SIZE <= j
                    ):
                        click_pos[1] = j
                        break
                return click_pos
            else:
                return None
