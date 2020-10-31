import pygame

class Token:
    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'token_' + color + '.png'
        self.position = self.row*board.cols+self.col