import pygame
from .pawns import Pawn, Counter
from .tokens import Token
from .assets import sound


class Player:
    array = []
    total = 0

    def __init__(self, order, color):
        self.order = order
        self.color = color

        self.pawn = []
        self.token = []
        self.score = 0

        Player.array.append(self)

    def place_pawn(self, display, board, col, row):
        """
        Places one Pawn with the Player's color on the given position.
        1) col: Column of the position to place the Pawn.
        2) row: Row of the position to place the Pawn.
        """
        self.pawn.append(Pawn(self.color, col, row))
        self.get_queen_sound(board, col, row)
        sound("click2.wav")
        card = board.get_card(col, row)
        if card.activate(Player.array, card.col, card.row):
            display.print_all(board, self)
            if card.rank == "QUEEN":
                card.special(display, board)

    def place_token(self, col, row):
        """
        Places one Token with the Player's color on the given position.
        1) col: Column of the position to place the Token.
        2) row: Row of the position to place the Token.
        """
        self.token.append(Token(self.color, col, row))

    @classmethod
    def get_token(cls, col, row):
        """
        Returns the Token on the specified position.
        Returns None if there's no Token.
        1) col: Column of the position to check.
        2) row: Row of the position to check.

        """
        for player in cls.array:
            for token in player.token:
                if token.position == (col, row):
                    return token
        return None

    @classmethod
    def get_pawns(cls, col, row):
        """
        Returns a list with all Pawns on the specified position.
        Returns an empty list if there're no Pawns.
        1) col: Column of the position to check.
        2) row: Row of the position to check.
        """
        pawns_on_this_position = []
        for player in cls.array:
            for pawn in player.pawns:
                if pawn.position == (col, row):
                    pawns_on_this_position.append(pawn)
        return pawns_on_this_position

    @classmethod
    def _get_all_pawns_positions(cls):
        """
        Records all pawns current positions as previous.
        Used at the beginning of the round, to record the
        state of the board before moving so it can be
        checked if a card was just flipped or not
        """
        for player in cls.array:
            for pawn in player.pawn:
                pawn.previous = pawn.position

    def _get_pawn_on_screen(self, display, _pawn):
        """
        Get coordinates in pixels of the top left
        of a pawn on the screen. Used by select() and
        "display" methods.
        - pawn.index and self.order multiply PAWN_SIZE
            so pawns don't print over each other.
        """
        screen_pos_x = (
            (display.CORNER[0] + display.CARD_SIZE * (_pawn.col))
            + (display.PAWN_SIZE * self.pawn.index(_pawn))
            + display.CARD_BORDER
        )
        screen_pos_y = (
            (display.CORNER[1] + display.CARD_SIZE * (_pawn.row + 1))
            - (display.PAWN_SIZE * (self.order))
            - display.CARD_BORDER
        )
        return screen_pos_x, screen_pos_y

    def select(self, board, display, event):
        """Selects a pawn with a click."""
        mouse = pygame.mouse.get_pos()
        for pawn in self.pawn:
            screen_pos = self._get_pawn_on_screen(display, pawn)
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and screen_pos[0] <= mouse[0] <= screen_pos[0] + display.PAWN_SIZE
                and screen_pos[1] <= mouse[1] <= screen_pos[1] + display.PAWN_SIZE
            ):
                # Pawn Selected
                Pawn.selected = pawn
                sound("click1.wav")
                break
            else:
                Pawn.selected = False

    def get_rank_sound(self, board, col, row):
        card = board.get_card(col, row)
        if card.rank == "ROOK":
            sound("rook.wav")
        elif card.rank == "BISHOP":
            sound("bishop.wav")
        elif card.rank == "KNIGHT":
            sound("knight.wav")
        elif card.rank == "QUEEN":
            sound("queen.wav")

    def get_queen_sound(self, board, col, row):
        card = board.get_card(col, row)
        if card.rank == "QUEEN":
            sound("queen.wav")

    def move(self, display, board, event):
        """
        Attempts to moves a selected pawn to the new position
        and calls the Card activate and Card special methods.
        """
        position = board.get_click_to_pos(display, event)
        if position is not None:
            if not Pawn.selected._move(board, self, position[0], position[1]):
                # Failed to move. Unselected."
                Pawn.selected = False
                return False
            else:
                # Successful move.
                card = board.get_card(position[0], position[1])
                if card.activate(Player.array, card.col, card.row):
                    display.print_all(board, self)
                    if card.rank == "QUEEN":
                        card.special(display, board)
                Pawn.selected = False
                return True
        else:
            # Failed to move. Unselected."
            Pawn.selected = False
            return False

    def turn(self, display, board, event):
        """
        If there's a Pawn already selected, checks if the new clicked
        location is not the other Pawn of the player and then attempts
        to move.
        If there's no Pawn selected, calls select().
        """
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Pawn.selected:
                for pawn in self.pawn:
                    screen_pos = self._get_pawn_on_screen(display, pawn)
                    if (
                        screen_pos[0] <= mouse[0] <= screen_pos[0] + display.PAWN_SIZE
                        and screen_pos[1]
                        <= mouse[1]
                        <= screen_pos[1] + display.PAWN_SIZE
                    ):
                        # Pawn Selected
                        Pawn.selected = pawn
                        sound("click1.wav")
                        return False
                if self.move(display, board, event):
                    return True
                else:
                    return False
            else:
                self.select(board, display, event)
                return False

    def recruit(self, board):
        """
        Checks if both pawns of a Player are on different
        cards of the same rank and color.
        1) board used for get_card() method.
        """
        card_0 = board.get_card(self.pawn[0].col, self.pawn[0].row)
        card_1 = board.get_card(self.pawn[1].col, self.pawn[1].row)
        token_0 = Player.get_token(self.pawn[0].col, self.pawn[0].row)
        token_1 = Player.get_token(self.pawn[1].col, self.pawn[1].row)
        if self.pawn[0].position != self.pawn[1].position:
            if card_0.color == card_1.color and card_0.rank == card_1.rank:
                if token_0 is not None and token_1 is not None:
                    # These cards were already recruited
                    return None
                else:
                    self.get_rank_sound(board, card_0.col, card_0.row)
                    self.place_token(self.pawn[0].col, self.pawn[0].row)
                    self.place_token(self.pawn[1].col, self.pawn[1].row)
                    self.score += 1
                    return self.order
        return None


class CounterKing(Player):
    def place_pawn(self, col, row):
        """Places the Counter Pawn."""
        sound("click2.wav")
        self.pawn.append(Counter(self.color, col, row))

    def _get_pawn_on_screen(self, display, *args):
        """
        Get pixel coordinates of the Counter Pawn on the
        screen (Top Left of the Cards).
        """
        return (
            (display.CORNER[0] + display.CARD_SIZE * (self.pawn[0].col))
            + display.CARD_BORDER,
            (display.CORNER[1] + display.CARD_SIZE * (self.pawn[0].row))
            + display.CARD_BORDER,
        )

    def recruit(self, board):
        """
        Checks if the Counter Pawn is on a card of the
        same rank and color of one of the Player's. If so:
        1) calls place_token() on the coordinates of both pawns
        2) increases the Counter score
        3) set Player.who_recruited to Counter order number
        """
        counter = self.pawn[0]
        card_counter = board.get_card(counter.col, counter.row)
        for pawn in Player.array[1].pawn:
            card_player = board.get_card(pawn.col, pawn.row)
            if (
                Player.get_token(counter.col, counter.row) is None
                and counter.position != pawn.position
                and card_counter.color == card_player.color
                and card_counter.rank == card_player.rank
            ):
                sound("counter.wav")
                self.place_token(counter.col, counter.row)
                self.place_token(pawn.col, pawn.row)
                self.score += 1
                return self.order
        return None
