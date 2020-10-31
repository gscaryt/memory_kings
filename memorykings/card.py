import pygame

class Card:
    def __init__(self, board_cols, position, color, rank, back):
        self.position = position
        self.color = color
        self.rank = rank
        self.back = back
        self.image = color + '_' + rank + '.png'
        self.recruited = None
        self.col = self.position % board_cols
        self.row = self.position // board_cols

    def get_position(self, board, col, row):
        return row*board.cols+col


    