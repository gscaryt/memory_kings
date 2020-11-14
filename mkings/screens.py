import pygame
import sys
from .constants import BACKGROUND, FPS, WHITE, FONTS_PATH
from .buttons import Button, Toggle
from .players import Player


def _text(font, text_input, x_center, y_center, color=WHITE):
    text = font.render(text_input, True, color)
    text_rect = text.get_rect()
    text_rect.center = (int(x_center), int(y_center))
    return text, text_rect


def start_menu(game, display):
    HINT = display.HINT*1.3
    DISP_W = display.DISP_W
    DISP_H = display.DISP_H

    clock = pygame.time.Clock()
    pygame.font.init()
    DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.20))
    DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.18))
    UBUNTU_R = pygame.font.Font(FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.10))

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
    grid = Toggle(
        DISP_W * 0.5,
        DISP_H * 0.5 - HINT * 0.5,
        HINT * 0.6,
        HINT * 0.2,
        game.choose_grid,
    )
    setup = Toggle(
        DISP_W * 0.5,
        DISP_H * 0.5 + HINT * 0.2,
        HINT * 0.6,
        HINT * 0.2,
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

    # TEXTS
    t1 = _text(
        DIMBO_L, "Number of Players", DISP_W * 0.5, DISP_H * 0.5 - HINT * 1.7
        )
    t2 = _text(
        DIMBO_L, "Grid Size", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.8
        )
    t21 = _text(
        DIMBO_R, "5x5", DISP_W * 0.5 - HINT * 0.5, DISP_H * 0.5 - HINT * 0.5
        )
    t22 = _text(
        DIMBO_R, "6x6", DISP_W * 0.5 + HINT * 0.5, DISP_H * 0.5 - HINT * 0.5
        )
    t3 = _text(
        DIMBO_L, "Setup Variant", DISP_W * 0.5, DISP_H * 0.5 - HINT * 0.1
        )
    t31 = _text(
        DIMBO_R, "Standard", DISP_W * 0.5 - HINT * 0.7, DISP_H * 0.5 + HINT * 0.2
        )
    t32 = _text(
        DIMBO_R, "Alternate", DISP_W * 0.5 + HINT * 0.7, DISP_H * 0.5 + HINT * 0.2
        )
    t4 = _text(
        UBUNTU_R, "v0.6 made by G. Scary T.", DISP_W * 0.86, DISP_H * 0.97
        )
    start_menu_text = t1, t2, t21, t22, t3, t31, t32, t4

    while game._creating:
        clock.tick(FPS)

        for event in pygame.event.get():
            display.WINDOW.fill((BACKGROUND))

            for text in start_menu_text:
                display.WINDOW.blit(*text)

            solo.lock_button(display.WINDOW, (game._num_of_players == 2))
            two.lock_button(display.WINDOW, (game._num_of_players == 3))
            three.lock_button(display.WINDOW, (game._num_of_players == 4))
            four.lock_button(display.WINDOW, (game._num_of_players == 5))
            grid.switch(display.WINDOW)
            setup.switch(display.WINDOW)
            logo.button(display.WINDOW)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.display.update()


def end_screen(display, game):
    _end_screen = True
    HINT = display.HINT*1.3
    DISP_W = display.DISP_W
    DISP_H = display.DISP_H

    pygame.font.init()
    DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT*0.5))
    DIMBO_R = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(HINT*0.2))

    if game._winner is not None:
        if Player.total == 2:
            if game._winner == game.counter:
                t1 = _text(
                    DIMBO_L, "You Lost!", DISP_W*0.5, DISP_H*0.5 - HINT*0.3
                )
                t2 = _text(
                    DIMBO_R,
                    f"The Counter King recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'}",
                    DISP_W*0.5,
                    DISP_H*0.5 + HINT*0.3,
                )
                t3 = _text(
                    DIMBO_R,
                    f"and reached the Card on {game._winner.pawn[0].col+1}, {game._winner.pawn[0].row+1}.",
                    DISP_W*0.5,
                    DISP_H*0.5 + HINT*0.55,
                )
            else:
                t1 = _text(
                    DIMBO_L, "You Won!", DISP_W*0.5, DISP_H*0.5 - HINT*0.3
                )
                t2 = _text(
                    DIMBO_R,
                    f"You recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'}.",
                    DISP_W*0.5,
                    DISP_H*0.5 + HINT*0.3,
                )
        else:
            t1 = _text(
                DIMBO_L,
                f"Player {game._winner.color} Won!",
                DISP_W*0.5,
                DISP_H*0.5 - HINT*0.3,
            )
            t2 = _text(
                DIMBO_R,
                f"{game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'} Recruited.",
                DISP_W*0.5,
                DISP_H*0.5 + HINT*0.3,
            )

    while _end_screen:
        if game._winner is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _end_screen = False
                display.WINDOW.fill((BACKGROUND))
                display.WINDOW.blit(*t1)
                display.WINDOW.blit(*t2)
                try:
                    display.WINDOW.blit(*t3)
                except UnboundLocalError:
                    pass

            pygame.display.update()

        else:
            return
