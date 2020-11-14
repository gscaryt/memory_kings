class Pawn:
    selected = None

    def __init__(self, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = "pawn_" + color + ".png"
        self.previous = None

    @property
    def position(self):
        return (self.col, self.row)

    def _move(self, board, Player, col, row):
        """
        If valid, moves the Pawn to new position.
        Used by move() on players.py.
        1) board: Board instance used by "check_move()"
        2) Player: Player object used by "check_move()"
        3) col: Destination column.
        4) row: Destination row.
        """
        if self.check_move(board, Player, col, row):
            self.col = col
            self.row = row
            return True
        else:
            return False

    def _is_to_adjacent(self, col, row):
        """
        Private for use in check_move().
        Returns True if new position is adjacent to the Pawn.
        1) col: Target column.
        2) row: Target row.
        """
        return (
            (col, row) == (self.col + 1, self.row)
            or (col, row) == (self.col - 1, self.row)
            or (col, row) == (self.col, self.row + 1)
            or (col, row) == (self.col, self.row - 1)
        )

    def check_move(self, board, Player, col, row):
        """
        Checks for the validity of a move.
        1) board: Board instance used by "get_card()"
        2) Player: Player object used by "get_token()"
        3) col: Destination column.
        4) row: Destination row.
        """
        if (col, row) == self.position: # Attempt to move to same position.
            return False
        elif self._is_to_adjacent(col, row):
            return True
        elif Player.get_token(self.col, self.row) is None:
            if board.get_card(self.col, self.row).is_valid_escort(col, row):
                return True
        elif Player.get_token(self.col, self.row).color == self.color:
            if board.get_card(self.col, self.row).is_valid_escort(col, row):
                return True
        return False


class Counter(Pawn):
    def _move(self, board):
        """
        Moves the Counter Pawn in a raster pattern
        from Card 0 down to the last card.
        """
        if self.row % 2 == 0 and not self.col == board.cols - 1:
            self.col = self.col + 1
        elif self.row % 2 != 0 and not self.col == 0:
            self.col = self.col - 1
        else:
            self.row = self.row + 1
