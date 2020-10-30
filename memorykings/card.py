import pygame

class Card:
    def __init__(self, position, color, rank, back, board_cols):
        self.position = position
        self.color = color
        self.rank = rank
        self.back = back
        self.image = color + '_' + rank + '.png'
        self.col = self.position % board_cols 
        self.row = self.position // board_cols

    def get_position(self, col, row, board_cols):
        return row*board_cols+col


    