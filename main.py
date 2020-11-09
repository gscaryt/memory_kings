import pygame
import time
from memorykings.constants import (
    EXTRA_WIDTH,
    EXTRA_HEIGHT,
    CORNER,
    CARD_SIZE,
    FPS,
    WHITE,
    DARK_GREY,
)
from memorykings.start_screen import start_menu
from memorykings.display import display
from memorykings.game import Game
from memorykings.cards import Card
from memorykings.players import Player
from memorykings.tokens import Token


def main():
    game = Game()
    start_menu(game)
    game.create_board()
    game.create_players()
    clock = pygame.time.Clock()
    run = True

    GAME_WINDOW = pygame.display.set_mode((game.WINDOW_WIDTH, game.WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Kings")

    # GAME_LOOP
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            GAME_WINDOW.fill(DARK_GREY)
            display.print_all(
                GAME_WINDOW,
                game.board,
                game.current_turn,
                game.pawn_selected,
                game.num_of_players,
                game.WINDOW_WIDTH,
                game.WINDOW_HEIGHT,
            )
            if event.type == pygame.QUIT:
                run = False
            if game.end_game_check():
                time.sleep(1)
                run = False
            else:
                if game.all_pawns_set is not True:
                    game.place_pawns(event)
                if game.all_pawns_set is True:
                    game.round(GAME_WINDOW, display)
                if game.end_turn is True:
                    game.change_turn()
    pygame.quit()
    quit()


main()
