import pygame
from .constants import (
    IMAGES_PATH, 
    CARD_SIZE, 
    PAWN_SIZE, 
    TOKEN_SIZE, 
    CORNER, 
    EXTRA_WIDTH, 
    EXTRA_HEIGHT, 
    PLAYER_COLOR_CODES
)
from .players import Player
from .pawns import Pawn

class Display:
    def __init__(self):
        self.width = 250
        self.height = 400
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Memory Kings")

    def set_game_window(self, board):
        self.width = EXTRA_WIDTH + board.cols * CARD_SIZE
        self.height = EXTRA_HEIGHT + board.rows * CARD_SIZE
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Memory Kings")

    def get_image(self, image, width, height):
        """Loads and returns an image with the given size"""
        return pygame.transform.scale(
            pygame.image.load(IMAGES_PATH + image).convert_alpha(), (width, height)
        )

    def print_grid(self, board):
        """
        Prints the board (grid of cards). Prints the face of any
        card with a token or a pawn on it and the back of any other
        """
        for row in range(board.rows):
            for col in range(board.cols):
                card = board.get_card(row, col)
                pos_on_screen = (
                    CORNER[0] + CARD_SIZE * card.col,
                    CORNER[1] + CARD_SIZE * card.row,
                )
                is_open = False

                for player in Player.array:
                    for pawn in player.pawn:
                        if pawn.position == card.position:
                            card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
                            self.window.blit(card_image, pos_on_screen)
                            is_open = True
                    for token in player.token:
                        if token.position == card.position:
                            card_image = self.get_image(
                                card.image, CARD_SIZE, CARD_SIZE
                            )
                            self.window.blit(card_image, pos_on_screen)
                            is_open = True

                if not is_open:
                    if card.back == "WHITE":
                        white_back = self.get_image("white_back.png", CARD_SIZE, CARD_SIZE)
                        self.window.blit(white_back, pos_on_screen)
                    elif card.back == "BLACK":
                        black_back = self.get_image("black_back.png", CARD_SIZE, CARD_SIZE)
                        self.window.blit(black_back, pos_on_screen)

    def print_pawns(self):
        """Gets and prints all placed pawns of all players"""
        for player in Player.array:
            for pawn in player.pawn:
                pos_on_screen = player._get_pawn_on_screen(pawn)
                pawn_image = self.get_image(
                    pawn.image, PAWN_SIZE, PAWN_SIZE
                )
                self.window.blit(pawn_image, pos_on_screen)
    
    def print_tokens(self):
        """Gets and prints all placed tokens of all players"""
        for player in Player.array:
            for token in player.token:
                pos_on_screen = (
                    int((CORNER[0] + CARD_SIZE * (1 + token.col))-TOKEN_SIZE*7/6),
                    int((CORNER[1] + CARD_SIZE * (token.row))+TOKEN_SIZE*1/5),
                )
                token_image = self.get_image(token.image, TOKEN_SIZE, TOKEN_SIZE)
                self.window.blit(token_image, pos_on_screen)

    def print_selected(self, current_player):
        """Prints a small highlight under the selected pawn."""
        if Pawn.selected:
            pos_on_screen = list(current_player._get_pawn_on_screen(Pawn.selected))
            pos_on_screen[0] -= PAWN_SIZE//5
            pos_on_screen[1] -= PAWN_SIZE//5
            pawn_image = self.get_image(
                "selected_shadow.png", PAWN_SIZE*7//5, PAWN_SIZE*7//5
            )
            self.window.blit(pawn_image, pos_on_screen)
    
    def print_invalid_moves(self, board):
        """
        Prints a "deny" sign over any card that can't be reached
        by the selected pawn
        """
        if Pawn.selected:
            for rows in board.grid:
                for card in rows:
                    pos_on_screen = (
                        CORNER[0] + CARD_SIZE * card.col,
                        CORNER[1] + CARD_SIZE * card.row,
                    )
                    if not Pawn.selected.check_move(
                        board, Player, card.col, card.row
                    ):
                        if card.position == Pawn.selected.position:
                            continue
                        else:
                            image = self.get_image("unavailable.png", CARD_SIZE, CARD_SIZE)
                            self.window.blit(image, pos_on_screen)

    def print_score_board(self):
        pygame.font.init()
        DIMBO_L = pygame.font.Font("fonts/dimbo_regular.ttf", CARD_SIZE//5)
        for i, player in enumerate(Player.array):
            t1 = DIMBO_L.render(f"{player.color}: {player.score}", True, PLAYER_COLOR_CODES[i])
            t1_rect = t1.get_rect()
            if Player.total == 2:
                t1_rect.center = (
                    (self.width // 2) - (CARD_SIZE / 2) + (i * CARD_SIZE),
                    self.height - CARD_SIZE//4,
                )
                self.window.blit(t1, t1_rect)
            else:
                if i != 0:
                    if Player.total == 3:
                        t1_rect.center = (
                            (self.width // 2) - (CARD_SIZE / 2) + ((i - 1) * CARD_SIZE),
                            self.height - CARD_SIZE//4,
                        )
                        self.window.blit(t1, t1_rect)
                    elif Player.total == 4:
                        t1_rect.center = (
                            (self.width // 2) - (CARD_SIZE) + ((i - 1) * CARD_SIZE),
                            self.height - CARD_SIZE//4,
                        )
                        self.window.blit(t1, t1_rect)
                    else:
                        t1_rect.center = (
                            (self.width // 2) - (3 * CARD_SIZE / 2) + ((i - 1) * CARD_SIZE),
                            self.height - CARD_SIZE//4,
                        )
                        self.window.blit(t1, t1_rect)
        pygame.display.update()

    def print_all(self, board, current_player):
        """
        Print all layers of the game in the order:
        grid > select pawn highlight > valid_moves > pawns > tokens
        """
        self.print_grid(board)
        self.print_selected(current_player)
        self.print_invalid_moves(board)
        self.print_pawns()
        self.print_tokens()
        self.print_score_board()
        pygame.display.update()

    def print_card(self, board, col, row):
        """Show one hidden card for 2 seconds and turns it back down."""
        card = board.grid[row][col]
        pos_on_screen = (
            CORNER[1] + CARD_SIZE * col,
            CORNER[0] + CARD_SIZE * row,
        )
        is_open = False
        for player in Player.array:
            for pawn in player.pawn:
                if pawn.position == card.position:
                    is_open = True
                    return False
            for token in player.token:
                if token.position == card.position:
                    is_open = True
                    return False
        if not is_open:
            card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
            self.window.blit(card_image, pos_on_screen)
            pygame.display.update()
            pygame.time.wait(2000)
            return True
