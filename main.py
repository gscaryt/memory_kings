import pygame
import time
from mkings.constants import (FPS, DARK_GREY)
from mkings.screens import start_menu
from mkings.display import Display
from mkings.game import Game


def main():
    game = Game()
    display = Display()
    start_menu(game, display)
    game.create_board()
    game.create_players()
    clock = pygame.time.Clock()
    run = True

    display.set_game_window(game.board)

    # GAME_LOOP
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            display.window.fill(DARK_GREY)
            display.print_all(game.board, game.current)
            if event.type == pygame.QUIT:
                run = False
            if game.is_end_game():
                time.sleep(1)
                run = False
            else:
                if game._all_pawns_set is not True:
                    game.place_pawns(event)
                if game._all_pawns_set is True:
                    game.round(display)
                if game.end_turn is True:
                    game.change_turn()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
