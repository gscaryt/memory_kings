import pygame
import logging as log
from .constants import CORNER, PAWN_SIZE, CARD_SIZE
from .pawn import Pawn
from .token import Token

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Player:
    def __init__(self, order, color):
        self.order = order
        self.color = color
        self.score = 0
        self.pawn = []
        self.token = []
        self.selected = -1

    # PLACEMENT

    def place_pawn(self, board, col, row):
        self.pawn.append(Pawn(board, self.color, col, row))

    def place_tokens(self, board, col, row, col2, row2):
        self.token.append(Token(board,self.color,col,row))
        self.token.append(Token(board,self.color,col2,row2))
        self.score += 1

    # CHECK

    def move_check(self, board, player_array, col, row):
        pawn = self.pawn[self.selected]
        card = board.card[pawn.position]
        if (col, row) == (pawn.col, pawn.row):
            ## Move to Same Location Attempt
            log.debug("move_check() - Move to Same Location attempt. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
            return False
        elif (
            ## Move as a Pawn (1 Orthogonal)
            (col, row) == (pawn.col+1, pawn.row) 
            or (col, row) == (pawn.col-1, pawn.row) 
            or (col, row) == (pawn.col, pawn.row+1) 
            or (col, row) == (pawn.col, pawn.row-1)
            ):
            log.debug(f"move_check() - Valid standard pawn move. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
            return True
        else:
            ## Move from an Opponent's Card
            for i in range(len(player_array)):
                for j in range(len(player_array[i].token)):
                    token = player_array[i].token[j]
                    if ((token.col, token.row) == (pawn.col, pawn.row)
                        and not self.color == token.color):
                        log.debug(f"move_check() - Opponent token in place. Cannot escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                        return False
            ## Bishop Escort
            if ((card.rank == "Bishop") 
                and (abs(col - pawn.col) == abs(row - pawn.row))
                ):
                log.debug(f"move_check() - Valid Bishop Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Rook Escort
            elif ((card.rank == "Rook") 
                and ((col == pawn.col) or (row == pawn.row))
                ):
                log.debug(f"move_check() - Valid Rook Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Knight Escort
            elif ((card.rank == "Knight") 
                and ((abs(col-pawn.col) == 2 and abs(row-pawn.row) == 1) 
                or (abs(col-pawn.col) == 1 and abs(row-pawn.row) == 2))
                ):
                log.debug(f"move_check() - Valid Knight Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Queen Escort
            elif ((card.rank== "Queen") 
                and ((abs(col - pawn.col) == abs(row - pawn.row))
                or ((col == pawn.col) or (row == pawn.row)))
                ):
                log.debug(f"move_check() - Valid Queen Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Invalid Move
            else:
                log.debug(f"move_check() - Invalid Move. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return False

    # SCREEN INTERACTION

    def get_pawn_screen_location(self, pawn_num):
        if self.color == 'COUNTER':
            return (
            (CORNER[0]+CARD_SIZE*(self.pawn[pawn_num].col))+(PAWN_SIZE*pawn_num)+5, 
            (CORNER[1]+CARD_SIZE*(self.pawn[pawn_num].row))-(PAWN_SIZE*(0))+5
            )
        else:
            return (
            (CORNER[0]+CARD_SIZE*(self.pawn[pawn_num].col))+(PAWN_SIZE*pawn_num)+5, 
            (CORNER[1]+CARD_SIZE*(self.pawn[pawn_num].row+1))-(PAWN_SIZE*(self.order))-5
            )

    # SELECT AND/OR MOVE

    def select_or_move(self, game, board, player_array):
        turn = game.turn
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if turn == 0:
            game.change_turn()
        elif turn == self.order:
            if self.selected != -1:
                if not self.move(game, board, player_array):
                    log.debug(f'select_pawn() - Failed to move. Unselected.')
                    self.selected = -1
            else:
                for pawn_num in range(len(self.pawn)):
                    coords = self.get_pawn_screen_location(pawn_num)
                    log.debug(f'select_pawn() - Pawn {pawn_num}: {coords}')
                    log.debug(
                        f'select_pawn() - {click[0] == 1}'
                        f' {coords[0]-PAWN_SIZE < mouse[0] < coords[0]+PAWN_SIZE}'
                        f' and {coords[1]-PAWN_SIZE < mouse[1] < coords[1]+PAWN_SIZE}'
                        )
                    if (click[0] == 1 
                        and coords[0] < mouse[0] < coords[0]+PAWN_SIZE
                        and coords[1] < mouse[1] < coords[1]+PAWN_SIZE
                    ):
                        self.selected = pawn_num
                        log.debug(f'select_pawn() - Pawn Selected: {self.selected} is on the {game.board.card[self.pawn[self.selected].position].rank} Card')
                        break
                    else:
                        self.selected = -1

    def move(self, game, board, player_array):
        if self.selected != -1:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                coordinates = game.click_to_grid(board)
                if coordinates != None:
                    if self.move_check(board, player_array, coordinates[0], coordinates[1]):
                        self.pawn[self.selected].move_pawn(board, coordinates[0], coordinates[1])
                        self.selected = -1
                        game.change_turn()
                        return True
                    else:
                        self.selected = -1
                        return False
                else:
                    self.selected = -1
                    return False