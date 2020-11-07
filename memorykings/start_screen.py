import pygame
from .constants import DARK_GREY, FPS, IMAGES_PATH, WHITE, CORNER
from .buttons import Button, Toggle
from .players import Player


def start_menu(game):
    WIDTH, HEIGHT = 250, 400
    GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Kings")
    BACKGROUND = DARK_GREY
    clock = pygame.time.Clock()
    pygame.font.init()
    DIMBO_L = pygame.font.Font('fonts/dimbo_regular.ttf', 20)
    DIMBO_R = pygame.font.Font('fonts/dimbo_regular.ttf', 18)
    UBUNTU_R = pygame.font.Font('fonts/ubuntu_regular.ttf', 10)

    # BUTTONS
    solo = Button(
        'players_one.png',
        50, 60, 40, 40,
        'players_one_hover.png',
        game.choose_players, 1
        )
    two = Button(
        'players_two.png',
        100, 60, 40, 40,
        'players_two_hover.png',
        game.choose_players, 2
        )
    three = Button(
        'players_three.png',
        150, 60, 40, 40,
        'players_three_hover.png',
        game.choose_players, 3
        )
    four = Button(
        'players_four.png',
        200, 60, 40, 40,
        'players_four_hover.png',
        game.choose_players, 4)
    grid = Toggle(
        'toggle_left.png',
        125, 130, 60, 20,
        'toggle_right.png',
        game.choose_grid)
    setup = Toggle(
        'toggle_left.png',
        125, 200, 60, 20,
        'toggle_right.png',
        game.choose_setup
        )
    logo = Button(
        'mk_logo.png',
        125, 300, 150, 150,
        'mk_logo_hover.png',
        game.play_game
        )

    # TEXTS
    t1 = DIMBO_L.render('Number of Players', True, WHITE)
    t1_rect = t1.get_rect()
    t1_rect.center = (WIDTH//2, 25)

    t2 = DIMBO_L.render('Grid Size', True, WHITE)
    t2_rect = t2.get_rect()
    t2_rect.center = (WIDTH//2, 100)
    t21 = DIMBO_R.render('5x5', True, WHITE)
    t21_rect = t21.get_rect()
    t21_rect.center = (WIDTH//2-50, 130)
    t22 = DIMBO_R.render('6x6', True, WHITE)
    t22_rect = t22.get_rect()
    t22_rect.center = (WIDTH//2+50, 130)

    t3 = DIMBO_L.render('Setup Variant', True, WHITE)
    t3_rect = t3.get_rect()
    t3_rect.center = (WIDTH//2, 170)
    t31 = DIMBO_R.render('Standard', True, WHITE)
    t31_rect = t31.get_rect()
    t31_rect.center = (WIDTH//2-70, 200)
    t32 = DIMBO_R.render('Alternate', True, WHITE)
    t32_rect = t32.get_rect()
    t32_rect.center = (WIDTH//2+70, 200)

    t4 = UBUNTU_R.render('v0.6 made by G. Scary T.', True, WHITE)
    t4_rect = t4.get_rect()
    t4_rect.bottomright = (WIDTH-5, HEIGHT-5)


    while game.creating:
        clock.tick(FPS)

        
        for event in pygame.event.get():
            GAME_WINDOW.fill((BACKGROUND))

            GAME_WINDOW.blit(t1, t1_rect)
            solo.button(GAME_WINDOW)
            two.button(GAME_WINDOW)
            three.button(GAME_WINDOW)
            four.button(GAME_WINDOW)

            GAME_WINDOW.blit(t2, t2_rect)
            GAME_WINDOW.blit(t21, t21_rect)
            GAME_WINDOW.blit(t22, t22_rect)
            grid.switch(GAME_WINDOW)

            GAME_WINDOW.blit(t3, t3_rect)
            GAME_WINDOW.blit(t31, t31_rect)
            GAME_WINDOW.blit(t32, t32_rect)
            setup.switch(GAME_WINDOW)

            logo.button(GAME_WINDOW)
            GAME_WINDOW.blit(t4, t4_rect)
            
            if event.type == pygame.QUIT:
                pygame.quit()
            pygame.display.update()