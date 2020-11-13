import pygame
import time
from mkings.constants import FPS, BACKGROUND
from mkings.screens import start_menu, end_screen
from mkings.display import Display
from mkings.game import Game


def main():
    game = Game()
    run = True

    display = Display()
    clock = pygame.time.Clock()

    start_menu(game, display)
    game.create_board()
    game.create_players()

    display.set_game_window(game.board)

    # GAME_LOOP
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            display.window.fill(BACKGROUND)
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

    end_screen(display, game)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
