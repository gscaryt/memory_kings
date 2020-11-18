import pygame
import sys
from .constants import BACKGROUND, FPS, WHITE, FONTS_PATH
from .buttons import Button
from .players import Player


class ScreenManager:
    def __init__(self):
        self._start_menu = False
        self._run = False
        self._end_screen = False
        self._about_screen = False

    def _start_game(self):
        self._start_menu = False

    def _call_about(self):
        if self._about_screen is False:
            self._about_screen = True
        else:
            self._about_screen = False


    def start_menu(self, game, display):
        self._start_menu = True
        clock = pygame.time.Clock()
        pygame.event.clear()
        pygame.font.init()

        while self._start_menu:
            clock.tick(FPS)
            HINT = display.HINT * 1.5
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            # BUTTONS
            solo = Button(
                DISP_W * 0.5 - HINT * 0.75,
                DISP_H * 0.5 - HINT * 1.3,
                HINT * 0.4,
                HINT * 0.4,
                "players_one.png",
                "players_one_hover.png",
                game.choose_players,
                1,
            )
            two = Button(
                DISP_W * 0.5 - HINT * 0.25,
                DISP_H * 0.5 - HINT * 1.3,
                HINT * 0.4,
                HINT * 0.4,
                "players_two.png",
                "players_two_hover.png",
                game.choose_players,
                2,
            )
            three = Button(
                DISP_W * 0.5 + HINT * 0.25,
                DISP_H * 0.5 - HINT * 1.3,
                HINT * 0.4,
                HINT * 0.4,
                "players_three.png",
                "players_three_hover.png",
                game.choose_players,
                3,
            )
            four = Button(
                DISP_W * 0.5 + HINT * 0.75,
                DISP_H * 0.5 - HINT * 1.3,
                HINT * 0.4,
                HINT * 0.4,
                "players_four.png",
                "players_four_hover.png",
                game.choose_players,
                4,
            )
            grid = Button(
                DISP_W * 0.5,
                DISP_H * 0.5 - HINT * 0.5,
                HINT * 0.6,
                HINT * 0.2,
                "toggle_left.png",
                "toggle_right.png",
                game.choose_grid,
            )
            setup = Button(
                DISP_W * 0.5,
                DISP_H * 0.5 + HINT * 0.2,
                HINT * 0.6,
                HINT * 0.2,
                "toggle_left.png",
                "toggle_right.png",
                game.choose_setup,
            )
            logo = Button(
                DISP_W * 0.5,
                DISP_H * 0.5 + HINT * 1.2,
                HINT * 1.5,
                HINT * 1.5,
                "mk_logo.png",
                "mk_logo_hover.png",
                self._start_game,
            )

            for event in pygame.event.get():
                display.WINDOW.fill((BACKGROUND))

                DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.20))
                DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.18))
                UBUNTU_R = pygame.font.Font(FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.10))
                blit_text(display.WINDOW, DIMBO_L, "Number of Players", DISP_W * 0.5, DISP_H * 0.5 - HINT * 1.7)
                blit_text(display.WINDOW, DIMBO_L, "Grid Size", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.8)
                blit_text(display.WINDOW, DIMBO_R, "5x5", DISP_W * 0.5 - HINT * 0.5, DISP_H * 0.5 - HINT * 0.5)
                blit_text(display.WINDOW, DIMBO_R, "6x6", DISP_W * 0.5 + HINT * 0.5, DISP_H * 0.5 - HINT * 0.5)
                blit_text(display.WINDOW, DIMBO_L, "Setup Variant", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.1)
                blit_text(display.WINDOW, DIMBO_R, "Standard", DISP_W * 0.5 - HINT * 0.7, DISP_H * 0.5 + HINT * 0.2)
                blit_text(display.WINDOW, DIMBO_R, "Alternate", DISP_W * 0.5 + HINT * 0.7, DISP_H * 0.5 + HINT * 0.2)
                blit_text(display.WINDOW, UBUNTU_R, "v0.7 made by G. Scary T.", DISP_W * 0.99, DISP_H * 0.99, 'bottomright')

                solo.switch(display.WINDOW, (game._num_of_players == 2))
                two.switch(display.WINDOW, (game._num_of_players == 3))
                three.switch(display.WINDOW, (game._num_of_players == 4))
                four.switch(display.WINDOW, (game._num_of_players == 5))
                grid.toggle(display.WINDOW, (game._grid_size == (6,6)))
                setup.toggle(display.WINDOW, (game._setup_variant == "alternate"))
                logo.button(display.WINDOW)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)

            pygame.display.update()


    def game_screen(self, game, display):
        self._run = True
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        clock = pygame.time.Clock()
        pygame.event.clear()

        while self._run:
            clock.tick(FPS)
            for event in pygame.event.get():
                display.print_all(game.board, game.current)
                
                if event.type == pygame.QUIT:
                    game._abandoned = True
                    self._run = False

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)

                if game.is_end_game():
                    pygame.time.wait(500)
                    self._run = False
                else:
                    if game._all_pawns_set is not True:
                        game.place_pawns(display, event)
                    if game._all_pawns_set is True:
                        game.round(display)
                    if game.end_turn is True:
                        game._turns += 1
                        game.change_turn()


    def end_screen(self, game, display):
        self._end_screen = True
        clock = pygame.time.Clock()
        pygame.event.clear()
        pygame.font.init()

        while self._end_screen:
            clock.tick(FPS)

            # ABBREVIATIONS
            HINT = display.HINT * 1.5 # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            # BUTTON
            replay = Button(
                DISP_W * 0.5,
                DISP_H * 0.5 + HINT * 0.7,
                HINT * 0.4,
                HINT * 0.4,
                "replay.png",
                "replay_hover.png",
                game._reset,
            )

            # ACTUAL SCREEN
            if game._winner is not None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._end_screen = False

                    if event.type == pygame.VIDEORESIZE:
                        size = pygame.display.get_window_size()
                        display._resize(game.board, size)

                pygame.draw.rect(display.WINDOW, (20, 20, 20, 100), (0, DISP_H//4, DISP_W, DISP_H//2))

                DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.5))
                DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.2))
                if Player.total == 2:
                    if game._winner == game.counter:
                        blit_text(display.WINDOW, DIMBO_L, "You Lost!", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.5)
                        if game._winner.score >= 6:
                            blit_text(display.WINDOW,DIMBO_R,f"The Counter King recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair.'}",DISP_W * 0.5,DISP_H * 0.5 + HINT * 0.1)
                        else:
                            blit_text(display.WINDOW,DIMBO_R,f"The Counter King reached the last card of the grid.",DISP_W * 0.5, DISP_H * 0.5 + HINT * 0.1)
                    else:
                        blit_text(display.WINDOW, DIMBO_L, "You Won!", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.5)
                        blit_text(display.WINDOW,DIMBO_R,f"You recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'}.",DISP_W * 0.5,DISP_H * 0.5 + HINT * 0.1)
                else:
                    blit_text(display.WINDOW,DIMBO_L,f"Player {game._winner.color} Won!",DISP_W * 0.5,DISP_H * 0.5 - HINT * 0.5)
                    blit_text(display.WINDOW,DIMBO_R,f"{game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'} Recruited.",DISP_W * 0.5, DISP_H * 0.5 + HINT * 0.1)

                replay.button(display.WINDOW)
                pygame.display.update()
            else:
                return


    def about_screen(self, game, display):
        self._about_screen = True

        while self._about_screen:
            for event in pygame.event.get():
                display.WINDOW.fill((BACKGROUND))

                DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.20))
                DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.18))
                UBUNTU_R = pygame.font.Font(FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.10))
                blit_text(display.WINDOW, DIMBO_L, "About", DISP_W * 0.5, DISP_H * 0.5 - HINT * 1.7)
                blit_long_text(display.WINDOW, "In Memory Kings, players challenge their memory in this mix of the classic games of Chess and Pairs (a.k.a. memory®). They move their pawns strategically across a grid of hidden cards, revealing them, and finding indentical pairs. The player that finds the most pairs wins!", (HINT*0.5, DISP_H*0.5-HINT*1.5), UBUNTU_R, HINT*0.5)


                about = Button(
                    DISP_W * 0.99,
                    DISP_H * 0.99,
                    HINT * 0.2,
                    HINT * 0.2,
                    "players_four.png",
                    "players_four_hover.png",
                    self._call_about(),
                )

                logo.button(display.WINDOW)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)

                pygame.display.update()

# UTILITARY FUNCTIONS

def blit_text(surface, font, text_input, x, y, relative_to='center', color=WHITE):
    text = font.render(text_input, True, color)
    text_rect = text.get_rect()
    if relative_to == 'center':
        text_rect.center = (int(x), int(y))
    elif relative_to == 'topright':
        text_rect.topright = (int(x), int(y))
    elif relative_to == 'topleft':
        text_rect.topleft = (int(x), int(y))
    elif relative_to == 'bottomright':
        text_rect.bottomright = (int(x), int(y))
    elif relative_to == 'bottomleft':
        text_rect.bottomleft = (int(x), int(y))
    else:
        text_rect.center = (int(x), int(y))
    surface.blit(text, text_rect)


def blit_image(surface, image, pos, width, height):
    loaded = pygame.image.load(IMAGES_PATH + image).convert_alpha()
    scaled = pygame.transform.scale(loaded, (int(width), int(height)))
    rect = scaled.get_rect()
    x, y = pos
    rect.center = (x,y)
    surface.blit(scaled, rect)


def blit_long_text(surface, text, pos, font, x_padding=0, color=WHITE):
    '''
    Adapted from Ted Klein Bergman on StackOverflow.
    '''
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width-x_padding:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height