import pygame
import time
from .constants import (
    CARD_SIZE,
    IMAGES_PATH,
    CORNER,
    PAWN_SIZE,
    TOKEN_SIZE,
    WHITE,
    ORANGE,
    PURPLE,
    BROWN,
    GREY,
)
from .players import Player
from .cards import Card
from .tokens import Token


class Display:
    def get_image(self, image, width, height):
        """Loads and returns an image with the given size"""
        return pygame.transform.scale(
            pygame.image.load(IMAGES_PATH + image).convert_alpha(), (width, height)
        )

    def print_grid(self, window, board):
        """
        Prints the board (grid of cards). Prints the face of any
        card with a token or a pawn on it and the back of any other
        """
        for i in range(board.cols * board.rows):
            card = Card.deck[i]
            coords_on_screen = (
                CORNER[0] + CARD_SIZE * card.col,
                CORNER[1] + CARD_SIZE * card.row,
            )
            is_open = False
            for player in Player.array:
                for pawn in player.pawn:
                    for token in player.token:
                        if token.position == card.position:
                            card_image = self.get_image(
                                card.image, CARD_SIZE, CARD_SIZE
                            )
                            window.blit(card_image, coords_on_screen)
                            is_open = True
                    if pawn.position == card.position:
                        card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
                        window.blit(card_image, coords_on_screen)
                        is_open = True
            if not is_open:
                if card.back == "WHITE":
                    white_back = self.get_image("white_back.png", CARD_SIZE, CARD_SIZE)
                    window.blit(white_back, coords_on_screen)
                elif card.back == "BLACK":
                    black_back = self.get_image("black_back.png", CARD_SIZE, CARD_SIZE)
                    window.blit(black_back, coords_on_screen)

    def print_pawns(self, window):
        """Gets and prints all placed pawns of all players"""
        for player_num, player in enumerate(Player.array):
            for pawn_num, pawn in enumerate(player.pawn):
                coords_on_screen = pawn.get_screen_location(player_num)
                pawn_image = self.get_image(
                    player.pawn[pawn_num].image, PAWN_SIZE, PAWN_SIZE
                )
                window.blit(pawn_image, coords_on_screen)

    def print_tokens(self, window):
        """Gets and prints all placed tokens of all players"""
        for player in Player.array:
            for token in player.token:
                coords_on_screen = (
                    (CORNER[0] + CARD_SIZE * (1 + token.col)) - TOKEN_SIZE - 5,
                    (CORNER[1] + CARD_SIZE * (token.row)) + TOKEN_SIZE - 15,
                )
                token_image = self.get_image(token.image, TOKEN_SIZE, TOKEN_SIZE)
                window.blit(token_image, coords_on_screen)

    def print_selected(self, window, current_turn, pawn_selected):
        """Prints a small highlight under the selected pawn."""
        if pawn_selected is not False:
            coords_on_screen = list(pawn_selected.get_screen_location(current_turn))
            coords_on_screen[0] -= 6
            coords_on_screen[1] -= 6
            pawn_image = self.get_image(
                "selected_shadow.png", PAWN_SIZE + 12, PAWN_SIZE + 12
            )
            window.blit(pawn_image, coords_on_screen)

    def print_invalid_moves(self, window, board, pawn_selected):
        """
        Prints a "deny" sign over any card that can't be reached
        by the selected pawn
        """
        if pawn_selected is not False:
            for i in range(board.cols * board.rows):
                card = Card.deck[i]
                coords_on_screen = (
                    CORNER[0] + CARD_SIZE * card.col,
                    CORNER[1] + CARD_SIZE * card.row,
                )
                if not pawn_selected.move_check(
                    Card.deck, Token.array, card.col, card.row
                ):
                    if card.position == pawn_selected.position:
                        pass
                    else:
                        image = self.get_image("unavailable.png", CARD_SIZE, CARD_SIZE)
                        window.blit(image, coords_on_screen)

    def print_card(self, window, board, col, row):
        """Show one hidden card for 2 seconds and turns it back down."""
        card = board.grid[row][col]
        coords_on_screen = (
            CORNER[0] + CARD_SIZE * col,
            CORNER[1] + CARD_SIZE * row,
        )
        is_open = False
        for player in Player.array:
            for pawn in player.pawn:
                for token in player.token:
                    if token.position == card.position:
                        is_open = True
                        return False
                if pawn.position == card.position:
                    is_open = True
                    return False
        if not is_open:
            card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
            window.blit(card_image, coords_on_screen)
            pygame.display.update()
            time.sleep(2)
            return True

    def print_score_board(self, window, num_of_players, width, height):
        pygame.font.init()
        DIMBO_L = pygame.font.Font("fonts/dimbo_regular.ttf", 20)
        COLORS = BROWN, ORANGE, PURPLE, GREY, WHITE
        for i, player in enumerate(Player.array):
            t1 = DIMBO_L.render(f"{player.color}: {player.score}", True, COLORS[i])
            t1_rect = t1.get_rect()
            if num_of_players == 2:
                t1_rect.center = (
                    (width // 2) - (CARD_SIZE / 2) + (i * CARD_SIZE),
                    height - 25,
                )
                window.blit(t1, t1_rect)
            else:
                if i != 0:
                    if num_of_players == 3:
                        t1_rect.center = (
                            (width // 2) - (CARD_SIZE / 2) + ((i - 1) * CARD_SIZE),
                            height - 25,
                        )
                        window.blit(t1, t1_rect)
                    elif num_of_players == 4:
                        t1_rect.center = (
                            (width // 2) - (CARD_SIZE) + ((i - 1) * CARD_SIZE),
                            height - 25,
                        )
                        window.blit(t1, t1_rect)
                    else:
                        t1_rect.center = (
                            (width // 2) - (3 * CARD_SIZE / 2) + ((i - 1) * CARD_SIZE),
                            height - 25,
                        )
                        window.blit(t1, t1_rect)
        pygame.display.update()

    def print_all(
        self, window, board, current_turn, pawn_selected, num_of_players, width, height
    ):
        """
        Print all layers of the game in the order:
        grid > select pawn highlight > valid_moves > pawns > tokens
        """
        self.print_grid(window, board)
        self.print_selected(window, current_turn, pawn_selected)
        self.print_invalid_moves(window, board, pawn_selected)
        self.print_pawns(window)
        self.print_tokens(window)
        self.print_score_board(window, num_of_players, width, height)
        pygame.display.update()


display = Display()
