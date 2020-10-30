import pygame

class Token:
    def __init__(self, color, col, row, board_cols):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'token_' + color + '.png'
        self.position = self.row*board_cols+self.col