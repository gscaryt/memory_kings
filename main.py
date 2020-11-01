import pygame, time
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
    game.setup_board(5,5)
    game.choose_colors()
    game.create_players(1)
    main_screen = Display()

    # SIMPLIFYING CALLS
    board = game.board
    player = game.player # Array containing all players.
    
    # GAME_LOOP
    while run:

        for event in pygame.event.get():
            if game.end_game_check():
                time.sleep(3)
                run = False

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.all_pawns_set:
                    game.place_pawns()
                else:
                    if game.turn == 0 and len(player) == 2:
                        game.counter_move()
                    else:
                        game.select_or_move()
                    
                if game.all_pawns_set:
                    game.counter_recruit()
                    game.recruit_check()
                
                if game.next_turn == True:
                    game.change_turn()
                            
            main_screen.print_grid(GAME_WINDOW, board, player)
            main_screen.print_pawns(GAME_WINDOW, player)
            main_screen.print_tokens(GAME_WINDOW, player)
            pygame.display.update()

    pygame.quit()

main()
