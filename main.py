import pygame
import sys
from mkings.constants import FPS, BACKGROUND
from mkings.screens import start_menu, end_screen
from mkings.display import Display
from mkings.game import Game
from mkings.stats import Stats

def main():
    game = Game()
    stats = Stats()
    run = True
    display = Display(100)
    clock = pygame.time.Clock()

    # START MENU WINDOW
    start_menu(game, display)
    stats.collect_start_data(game)

    # GENERATE BOARD AND PLAYERS
    game.create_board()
    game.create_players()
    display._set_corner(game.board)

    # MAIN LOOP
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            display.WINDOW.fill(BACKGROUND)
            display.print_all(game.board, game.current)
            
            if event.type == pygame.QUIT:
                game._abandoned = True
                run = False

            if event.type == pygame.VIDEORESIZE:
                size = pygame.display.get_window_size()
                display._resize(game.board, size)

            if game.is_end_game():
                pygame.time.wait(500)
                run = False
            else:
                if game._all_pawns_set is not True:
                    game.place_pawns(display, event)
                if game._all_pawns_set is True:
                    game.round(display)
                if game.end_turn is True:
                    game._turns += 1
                    game.change_turn()
    
    # END GAME WINDOW
    stats.collect_end_data(game)
    stats.write_data()
    end_screen(game, display)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
