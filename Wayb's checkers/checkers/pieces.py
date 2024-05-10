import pygame
from .constants import square_size, grey, light_blue, dark_blue, dark_green, dark_purple, crown, shiny_dark_red

class Piece:
    padding = 14
    outline = 2
    def __init__(self,row,col,color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_position()

    def calc_position(self):
        self.x = square_size * self.col + square_size // 2
        self.y = square_size * self.row + square_size // 2

    def make_king(self):
        self.king = True

    def draw(self,window):
        radius = square_size//2 - self.padding
        pygame.draw.circle(window, shiny_dark_red, (self.x, self.y), radius + self.outline)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            window.blit(crown, (self.x - crown.get_width()//2, self.y - crown.get_width()//2))

    def move(self,row,col):
        self.row = row
        self.col = col
        self.calc_position()

    def __repr__(self):
        return str(self.color)