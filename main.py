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
    game.choose_colors('ORANGE', 'PURPLE')
    game.create_players(1)


    # SIMPLIFYING CALLS
    board = game.board
    player = game.player # Array containing all players.

    # SETUP PAWNS
    # log.debug(f'Pawn 0: {player[1].pawn[0].position} Pawn 1: {player[1].pawn[1].position} Counter: {player[0].pawn[0].position}')
    main_screen = Display()
    
    # GAME_LOOP
    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.all_pawns_set:
                    game.place_pawns(board)
                elif game.turn == 0 and len(game.player) == 2:
                    game.counter_move(board)
                else:
                    player[game.turn].select_or_move(game, board, player)

            main_screen.print_grid(GAME_WINDOW, board, player)
            main_screen.print_pawns(GAME_WINDOW, player)
            main_screen.print_tokens(GAME_WINDOW, player)
            pygame.display.update()

    pygame.quit()

main()
