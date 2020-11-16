import pygame
import sys
from .constants import BACKGROUND, FPS, WHITE, FONTS_PATH
from .buttons import Button
from .players import Player


def _text(font, text_input, x, y, relative_to='center', color=WHITE):
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
    return text, text_rect


def start_menu(game, display):
    clock = pygame.time.Clock()
    pygame.event.clear()
    pygame.font.init()

    while game._creating or game._reset_game:
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
            game.play_game,
        )

        # FONTS AND TEXT
        DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.20))
        DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.18))
        UBUNTU_R = pygame.font.Font(FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.10))

        t1 = _text(DIMBO_L, "Number of Players", DISP_W * 0.5, DISP_H * 0.5 - HINT * 1.7)
        t2 = _text(DIMBO_L, "Grid Size", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.8)
        t21 = _text(DIMBO_R, "5x5", DISP_W * 0.5 - HINT * 0.5, DISP_H * 0.5 - HINT * 0.5)
        t22 = _text(DIMBO_R, "6x6", DISP_W * 0.5 + HINT * 0.5, DISP_H * 0.5 - HINT * 0.5)
        t3 = _text(DIMBO_L, "Setup Variant", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.1)
        t31 = _text(
            DIMBO_R, "Standard", DISP_W * 0.5 - HINT * 0.7, DISP_H * 0.5 + HINT * 0.2
        )
        t32 = _text(
            DIMBO_R, "Alternate", DISP_W * 0.5 + HINT * 0.7, DISP_H * 0.5 + HINT * 0.2
        )
        t4 = _text(UBUNTU_R, "v0.6 made by G. Scary T.", DISP_W * 0.99, DISP_H * 0.99, 'bottomright')
        start_menu_text = t1, t2, t21, t22, t3, t31, t32, t4

        # ACTUAL SCREEN

        for event in pygame.event.get():
            display.WINDOW.fill((BACKGROUND))

            for text in start_menu_text:
                display.WINDOW.blit(*text)

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


def end_screen(game, display):
    _end_screen = True
    pygame.event.clear()
    pygame.font.init()

    while _end_screen:

        # ABBREVIATIONS
        HINT = display.HINT * 1.5 # Magic number adjusts sizes without messing positions.
        DISP_W = display.DISP_W
        DISP_H = display.DISP_H
       
        # TEXTS
        if game._winner is not None:
            DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.5))
            DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.2))
            if Player.total == 2:
                if game._winner == game.counter:
                    t1 = _text(
                        DIMBO_L, "You Lost!", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.4
                    )
                    if game._winner.score >= 6:
                        t2 = _text(
                            DIMBO_R,
                            f"The Counter King recruited {game._winner.score}"
                            f" {'Pairs' if game._winner.score != 1 else 'Pair.'}",
                            DISP_W * 0.5,
                            DISP_H * 0.5 + HINT * 0.3,
                        )
                    else:
                        t2 = _text(
                            DIMBO_R,
                            f"The Counter King reached the last card of the grid.",
                            DISP_W * 0.5,
                            DISP_H * 0.5 + HINT * 0.3,
                        )
                else:
                    t1 = _text(DIMBO_L, "You Won!", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.3)
                    t2 = _text(
                        DIMBO_R,
                        f"You recruited {game._winner.score}"
                        f" {'Pairs' if game._winner.score != 1 else 'Pair'}.",
                        DISP_W * 0.5,
                        DISP_H * 0.5 + HINT * 0.3,
                    )
            else:
                t1 = _text(
                    DIMBO_L,
                    f"Player {game._winner.color} Won!",
                    DISP_W * 0.5,
                    DISP_H * 0.5 - HINT * 0.3,
                )
                t2 = _text(
                    DIMBO_R,
                    f"{game._winner.score}"
                    f" {'Pairs' if game._winner.score != 1 else 'Pair'} Recruited.",
                    DISP_W * 0.5,
                    DISP_H * 0.5 + HINT * 0.3,
                )

        replay = Button(
            DISP_W * 0.5,
            DISP_H * 0.5 + HINT * 0.8,
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
                    _end_screen = False

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)

                display.WINDOW.fill((BACKGROUND))
                display.WINDOW.blit(*t1)
                display.WINDOW.blit(*t2)
                replay.button(display.WINDOW)
            pygame.display.update()
        else:
            return
    