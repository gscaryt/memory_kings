import pygame
from memorykings.constants import WINDOW_WIDTH, WINDOW_HEIGHT, CORNER, CARD_SIZE
from memorykings.game import Game
from memorykings.display import Display

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Kings')

def main():
    # GENERATING GAME
    run = True
    game = Game()
    game.setup(5,5)
    game.choose_colors('ORANGE')
    game.create_players(1)

    # SIMPLIFYING CALLS
    board = game.board
    player = game.player # Array containing all players.

    # SETUP PAWNS
    player[0].place_pawn(board, 2, 4)
    player[1].place_pawn(board, 0, 0, )
    player[1].place_pawn(board, 3, 3)
    log.debug(f'Pawn 0: {player[1].pawn[0].position} Pawn 1: {player[1].pawn[1].position} Counter: {player[0].pawn[0].position}')
    main_screen = Display()
    
    # GAME_LOOP
    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.player[game.turn].selected == -1:
                    game.player[game.turn].select_pawn(game)
                else:
                    game.player[1].player_move(game, player, board)

            main_screen.print_grid(GAME_WINDOW, player, board)
            main_screen.print_pawns(GAME_WINDOW, player)
            main_screen.print_tokens(GAME_WINDOW, player)
            pygame.display.update()

    pygame.quit()

main()
