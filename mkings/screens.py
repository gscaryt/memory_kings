import pygame
import time
from .constants import DARK_GREY, FPS, WHITE
from .buttons import Button, Toggle
from .players import Player

def _text(font, text_input, x_center, y_center, color=WHITE):
    text = font.render(text_input, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x_center, y_center)
    return text, text_rect


def start_menu(game, display):
    BACKGROUND = DARK_GREY
    clock = pygame.time.Clock()
    pygame.font.init()
    DIMBO_L = pygame.font.Font("fonts/dimbo_regular.ttf", 20)
    DIMBO_R = pygame.font.Font("fonts/dimbo_regular.ttf", 18)
    UBUNTU_R = pygame.font.Font("fonts/ubuntu_regular.ttf", 10)

    # BUTTONS
    solo = Button(50,60,40,40,
        "players_one.png",
        "players_one_hover.png",
        game.choose_players,1)
    two = Button(100,60,40,40,
        "players_two.png",
        "players_two_hover.png",
        game.choose_players,2)
    three = Button(150,60,40,40,
        "players_three.png",
        "players_three_hover.png",
        game.choose_players,3)
    four = Button(200,60,40,40,
        "players_four.png",
        "players_four_hover.png",
        game.choose_players,4)
    grid = Toggle(125,130,60,20,
        game.choose_grid)
    setup = Toggle(125,200,60,20,
        game.choose_setup)
    logo = Button(125,300,150,150,
        "mk_logo.png",
        "mk_logo_hover.png",
        game.play_game)

    # TEXTS
    t1 = _text(DIMBO_L, "Number of Players", display.width // 2, 25)
    t2 = _text(DIMBO_L, "Grid Size", display.width // 2, 100)
    t21 = _text(DIMBO_R, "5x5", display.width // 2 - 50, 130)
    t22 = _text(DIMBO_R, "6x6", display.width // 2 + 50, 130)
    t3 = _text(DIMBO_L, "Setup Variant", display.width // 2, 170)
    t31 = _text(DIMBO_R, "Standard", display.width // 2 - 70, 200)
    t32 = _text(DIMBO_R, "Alternate", display.width // 2 + 70, 200)
    t4 = _text(UBUNTU_R, "v0.6 made by G. Scary T.", display.width - 5, display.height - 5)
    start_menu_text = t1,t2,t21,t22,t3,t31,t32,t4

    while game._creating:
        clock.tick(FPS)

        for event in pygame.event.get():
            display.window.fill((BACKGROUND))

            for text in start_menu_text:
                display.window.blit(*text)

            solo.button(display.window)
            two.button(display.window)
            three.button(display.window)
            four.button(display.window)
            grid.switch(display.window)
            setup.switch(display.window)
            logo.button(display.window)

            if event.type == pygame.QUIT:
                pygame.quit()
            pygame.display.update()


def end_screen(display, game):
    BACKGROUND = DARK_GREY
    display.width = 400
    display.height = 250
    display.window = pygame.display.set_mode((display.width, display.height))
    pygame.display.set_caption("Memory Kings")
    clock = pygame.time.Clock()
    _end_screen = True

    pygame.font.init()
    DIMBO_50 = pygame.font.Font("fonts/dimbo_regular.ttf", 50)
    DIMBO_20 = pygame.font.Font("fonts/dimbo_regular.ttf", 20)

    if Player.total == 2:
        if game.winner == game.counter:
            t1 = _text(DIMBO_50, "You Lost!",
                display.width // 2, display.height // 2 - 30)
            t2 = _text(DIMBO_20, f"The Counter King recruited {game.winner.score} {'Pairs' if game.winner.score != 1 else 'Pair'}",
                display.width // 2, display.height // 2 + 30)
            t3 = _text(DIMBO_20, f"and reached the Card on {game.winner.pawn[0].col+1}, {game.winner.pawn[0].row+1}.",
                display.width // 2, display.height // 2 + 55)
        else:
            t1 = _text(DIMBO_50, "You Won!",
                display.width//2, display.height // 2 - 30)
            t2 = _text(DIMBO_20, f"You recruited {game.winner.score} {'Pairs' if game.winner.score != 1 else 'Pair'}.",
                display.width//2, display.height // 2 + 30)
    else:
        t1 = _text(DIMBO_50, f"Player {game.winner.color} Won!",
            display.width//2, display.height // 2 - 30)
        t2 = _text(DIMBO_20, f"{game.winner.score} {'Pairs' if game.winner.score != 1 else 'Pair'} Recruited.",
            display.width//2, display.height // 2 + 30)

    while _end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            display.window.fill((BACKGROUND))
            display.window.blit(*t1)
            display.window.blit(*t2)
            try:
                display.window.blit(*t3)
            except Exception:
                pass
            pygame.display.update()

