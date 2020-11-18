import pygame
import random
from .constants import BACKS, RANKS, CARD_COLORS
from .cards import Card, Bishop, Rook, Knight, Queen

class Board:
    def __init__(self, cols, rows=None):
        self.cols = cols
        self.rows = rows if rows is not None else cols

        self.grid = []

    def gen_deck(self):
        """
        Generates all the Cards that are appended to the
        card array.
        Variable num_of_colors determines how many cards 
        need to be created based on the size of the board.
        """

        num_of_colors = int(
            (self.cols*self.rows - 1 + (self.cols*self.rows + 1) % 2)/(len(BACKS)*len(RANKS))
        )

        # GENERATE SPECIAL CARDS OUTSIDE THE LOOP
        Queen("", "QUEEN", "BLACK")

        # GENERATE CARD_SUB_CLASSES BASED ON THEIR RANK
        for back in BACKS:
            for rank in RANKS:
                for color in CARD_COLORS[:num_of_colors]:
                    if rank == "BISHOP":
                        Bishop(color, rank, back)
                    elif rank == "ROOK":
                        Rook(color, rank, back)
                    elif rank == "KNIGHT":
                        Knight(color, rank, back)
        
    def gen_grid(self, setup_variant):
        """
        Forms a grid with randomly placed cards.
        1) setup_variant: 
            1.1) "standard" for random placement.
            1.2) "alternate" for alternate placement.
        """
        random.shuffle(Card.array)
        if setup_variant == "alternate":
            Card.array = self._alternate_backs()
        for i, card in enumerate(Card.array):
            card.row = i // self.cols
            card.col = i % self.cols
        for j in range(0, len(Card.array), self.cols):
            grid_slice = Card.array[j: j + self.cols]
            self.grid.append(grid_slice)

    def _alternate_backs(self):
        """
        Organises the card list into a sequence of alternate backs.
        Used by the "alternate" setup_variant argument in gen_grid().
        """
        blacks = []
        whites = []
        for card in Card.array:
            if card.back == "BLACK":
                blacks.append(card)
            elif card.back == "WHITE":
                whites.append(card)

        alternate_deck = []
        B, W = 0, 0
        for j in range(self.rows):
            for i in range(self.cols):
                if i % 2 == j % 2:
                    alternate_deck.append(blacks[B])
                    B += 1
                else:
                    alternate_deck.append(whites[W])
                    W += 1

        return alternate_deck

    def get_card(self, col, row):
        """
        Finds the card on the given position.
        1) col: Column of the card.
        2) row: Row of the card.
        """
        try:
            return self.grid[row][col]
        except IndexError:
            return None

    def get_click_to_pos(self, display):
        """
        Converts the pixel coordinates of a mouse click
        to card coordinates in the grid.
        - Returns a (col, row) tuple.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0]:
            if not (
                mouse[0] < display.CORNER[0]
                or mouse[1] < display.CORNER[1]
                or mouse[1] > display.CORNER[1] + self.rows * display.CARD_SIZE
                or mouse[0] > display.CORNER[0] + self.cols * display.CARD_SIZE
            ):
                for i in range(self.cols):
                    if (
                        (mouse[0] - display.CORNER[0] - display.CARD_SIZE) / display.CARD_SIZE 
                        <= i <= 
                        (mouse[0] - display.CORNER[0]) / display.CARD_SIZE
                    ):
                        col = i
                        break
                for j in range(self.rows):
                    if (
                        (mouse[1] - display.CORNER[1] - display.CARD_SIZE) / display.CARD_SIZE 
                        <= j <= 
                        (mouse[1] - display.CORNER[1]) / display.CARD_SIZE
                    ):
                        row = j
                        break
                return col, row
            else:
                return None
