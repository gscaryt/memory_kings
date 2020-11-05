import pygame
from .constants import DARK_GREY, FPS
from .buttons import Button, Toggle

class NewGame():
    def __init__(self, num_of_players=1, grid_size=(5, 5), setup_variant='standard'):
        self.num_of_players = num_of_players
        self.grid_size = grid_size
        self.setup_variant = setup_variant

    def choose_players(self, number):
        self.num_of_players = number
        print(self.num_of_players)

    def choose_grid(self):
        if self.grid_size == (5, 5):
            self.grid_size = (6, 6)
            print(self.grid_size)
        else:
            self.grid_size = (5, 5)
            print(self.grid_size)

    def choose_setup(self):
        if self.setup_variant == 'standard':
            self.setup_variant = 'alternate'
            print(self.setup_variant)
        else:
            self.setup_variant = 'standard'
            print(self.setup_variant)

    def play_game(self):
        print('Start')
        self.creating = False
        return (self.num_of_players, self.grid_size)

def start_screen(start):
    GAME_WINDOW = pygame.display.set_mode((250, 400))
    pygame.display.set_caption("Memory Kings")
    start.creating = True
    clock = pygame.time.Clock()

    solo = Button('players_one.png', 50, 50, 40, 40, 'players_one_hover.png', start.choose_players, 1)
    two = Button('players_two.png', 100, 50, 40, 40, 'players_two_hover.png', start.choose_players, 2)
    three = Button('players_three.png', 150, 50, 40, 40, 'players_three_hover.png', start.choose_players, 3)
    four = Button('players_four.png', 200, 50, 40, 40, 'players_four_hover.png', start.choose_players, 4)
    grid = Toggle('toggle_left.png', 125, 125, 60, 20, 'toggle_right.png', start.choose_grid)
    setup = Toggle('toggle_left.png', 125, 180, 60, 20, 'toggle_right.png', start.choose_setup)
    logo = Button('mk_logo.png', 125, 300, 150, 150, 'mk_logo_hover.png', start.play_game)
    
    while start.creating:
        clock.tick(FPS)

        for event in pygame.event.get():
            GAME_WINDOW.fill((DARK_GREY))
            solo.button(GAME_WINDOW)
            two.button(GAME_WINDOW)
            three.button(GAME_WINDOW)
            four.button(GAME_WINDOW)
            grid.switch(GAME_WINDOW)
            setup.switch(GAME_WINDOW)
            logo.button(GAME_WINDOW)
            if event.type == pygame.QUIT:
                start.creating = False
            pygame.display.update()
