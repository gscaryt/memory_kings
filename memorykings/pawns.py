from .constants import CORNER, CARD_SIZE, CARD_BORDER, PAWN_SIZE

class Pawn:
    array = []

    def __init__(self, board, color, index, col, row):
        self.color = color
        self.index = index
        self.col = col
        self.row = row
        self.image = "pawn_" + self.color + ".png"
        self.position = self.row * board.cols + self.col
        self.previous = self.position
        Pawn.array.append(self)

    def move(self, board, card_array, token_array, col, row):
        """
        1) Calls move_check()
        2) if True, changes Pawn coordinates and position
        3) returns True or False
        """
        if self.move_check(card_array, token_array, col, row):
            self.col = col
            self.row = row
            self.position = row * board.cols + col
            return True
        else:
            return False

    def move_check(self, card_array, token_array, col, row):
        """
        Checks for the validity of a move.
        Returns True or False.
        """
        if (col, row) == (self.col, self.row):
            """Move to Same Location Attempt"""
            return False
        elif (
            (col, row) == (self.col + 1, self.row) or
            (col, row) == (self.col - 1, self.row) or
            (col, row) == (self.col, self.row + 1) or
            (col, row) == (self.col, self.row - 1)
        ):
            """Move as a Pawn (1 Orthogonal)"""
            return True
        elif card_array[self.position].escort_check(
            self, token_array, col, row
        ):
            """Calls escort_check method from the specific Card type."""
            return True
        else:
            return False

    def get_screen_location(self, player_order):
        """
        Get pixel coordinates of a pawn on the screen.
        Note: self.index and player_order are multiplying
        PAWN_SIZE so they don't print over each other.
        """
        return (
            (CORNER[0] + CARD_SIZE * (self.col)) +
            (PAWN_SIZE * self.index) +
            CARD_BORDER,
            (CORNER[1] + CARD_SIZE * (self.row + 1)) -
            (PAWN_SIZE * (player_order)) -
            CARD_BORDER,
        )


class Counter(Pawn):
    def __init__(self):
        self.color = "COUNTER"
        self.index = 0
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

    def get_screen_location(self, player_order):
        """
        Get pixel coordinates of the Counter Pawn on the
        screen (Top Left of the Cards).
        """
        return (
            (CORNER[0] + CARD_SIZE * (self.col)) + CARD_BORDER,
            (CORNER[1] + CARD_SIZE * (self.row)) + CARD_BORDER,
        )

