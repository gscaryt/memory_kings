import pygame

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

    def token_check(self, pawn, token_array, col, row):
        """
        Check to see if there is a token of a different player
        on the same card as the pawn trying to move and if they
        have the same color. A pawn cannot use Escort movement
        if the card has a token of an opponent.
        """
        if (
            self.get_token(token_array) is not None and
            self.get_token(token_array) != pawn.color
        ):
            return True

    def activate(self, player_array):
        """
        Check if a card was hidden or open when a pawn moves
        to it. Special powers (like the Queen's Peeking Card) only
        activate when a card is flipped from facing down to up.
        """
        for player in player_array:
            for pawn in player.pawn:
                for token in player.token:
                    if token.position == self.position:
                        return False
                if pawn.previous == self.position:
                    return False
        return True

    def special(self, *args, **kwargs):
        """Standard Cards have no special effects."""
        pass


class Bishop(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an token_check and then checks if the
        destination is on a diagonal from the card.
        """
        if not self.token_check(pawn, token_array, col, row):
            if abs(col - self.col) == abs(row - self.row):
                return True
            else:
                return False
        else:
            return False


class Rook(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an token_check and then checks if the
        destination is on a orthogonal from the card.
        """
        if self.token_check(pawn, token_array, col, row):
            return False
        else:
            if col == self.col or row == self.row:
                return True
            else:
                return False


class Knight(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an token_check and then checks if the
        destination is on an "L" pattern from the card.
        """
        if not self.token_check(pawn, token_array, col, row):
            if (abs(col - self.col) == 2 and abs(row - self.row) == 1) or (
                abs(col - self.col) == 1 and abs(row - self.row) == 2
            ):
                return True
            else:
                return False
        else:
            return False


class Queen(Card):
    def escort_check(self, pawn, token_array, col, row):
        """
        Calls an token_check and then checks if the
        destination is orthogonal or diagonal from the card.
        """
        if not self.token_check(pawn, token_array, col, row):
            if (abs(col - self.col) == abs(row - self.row)) or (
                (col == self.col) or (row == self.row)
            ):
                return True
            else:
                return False
        else:
            return False

    def special(self, window, display, board):
        """
        When the Queen is activated, the Player can
        peek any hidden card from the board.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = board.click_to_grid()
                    if click_pos is not None:
                        if not display.print_card(
                            window,
                            board,
                            click_pos[0],
                            click_pos[1],
                        ):
                            continue
                        else:
                            return True
