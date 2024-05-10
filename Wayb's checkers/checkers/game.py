import pygame
from .board import Board
from .constants import red, white, square_size, dark_blue

class Game:
    def __init__(self,window):
        self._init()
        self.window = window

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.turn = red
        self.selected = None
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self,row,col):
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row,col)
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False
    
    def _move(self,row,col):
        piece = self.board.get_piece(row,col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            self.board.move(self.selected, row,col)
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self,moves):
        for move in moves:
            row,col = move
            pygame.draw.circle(self.window, dark_blue,(col*square_size + square_size//2, row*square_size + square_size//2), 15)
    
    def change_turn(self):
        self.valid_moves = []
        self.turn = white if self.turn == red else red

    def winner(self):
        return self.board.winner()

    def get_board(self): #returns the current state of the board
        return self.board
    
    def ai_move(self,board):
        self.board = board
        self.change_turn()
