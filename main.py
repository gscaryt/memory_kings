import pygame
import sys
from mkings.constants import FPS, BACKGROUND
from mkings.screens import ScreenManager
from mkings.display import Display
from mkings.game import Game
from mkings.stats import Stats

def main():
    game = Game()
    stats = Stats()
    display = Display()
    screen_manager = ScreenManager()
    pygame.event.clear()

    # START MENU LOOP
    screen_manager.start_menu(game, display)

    # DATA COLLECTION START
    stats.collect_start_data(game)

    # GENERATE BOARD AND PLAYERS
    game.create_board()
    game.create_players()
    display._set_corner(game.board)

    # GAME LOOP
    screen_manager.game_screen(game, display)
    
    # DATA COLLECTION END
    stats.collect_end_data(game)
    stats.write_data()

    # END SCREEN LOOP
    screen_manager.end_screen(game, display)
    if game._reset_game is True:
        return main()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
