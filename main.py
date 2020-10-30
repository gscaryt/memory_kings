import pygame
from memorykings.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from memorykings.game import Game
from memorykings.screen import Screen

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Kings')

def main():
    run = True
    game = Game()
    game.setup(5,5)
    game.choose_colors('ORANGE')
    game.create_players(1)
    game.player[0].place_pawn(2, 4, game.board.cols)
    game.player[1].place_pawn(0, 0, game.board.cols)
    game.player[1].place_pawn(3, 3, game.board.cols)
    log.debug(f'Pawn 0: {game.player[1].pawn[0].position} Pawn 1: {game.player[1].pawn[1].position} Counter: {game.player[0].pawn[0].position}')
    game.player[1].place_tokens(1, 3, 4, 2, game.board.cols)
    log.debug(f'Token 0: {game.player[1].token[0].position} Token 1: {game.player[1].token[1].position}')
    screen = Screen()
    
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.player[game.turn].select_pawn(game.turn)
        
        screen.print_grid(GAME_WINDOW, game.board, game.player, game.board.card)
        screen.print_pawns(GAME_WINDOW, game.player)
        screen.print_tokens(GAME_WINDOW, game.player)
        pygame.display.update()

    pygame.quit()

main()
