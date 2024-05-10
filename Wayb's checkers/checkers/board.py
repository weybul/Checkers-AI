import pygame
from .constants import black, rows, square_size, red, cols, white
from . pieces import Piece

class Board:
    def __init__(self):
        self.board = []
        self.white_left = self.red_left = 12
        self.white_kings = self.red_kings = 0
        self.create_board()

    def draw_squares(self,window):
        window.fill(black)
        for row in range(rows):
            for col in range(row % 2, rows, 2):
                pygame.draw.rect(window, red, (row*square_size, col*square_size, square_size, square_size))

    def create_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, white))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, red))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self,window):
        self.draw_squares(window)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def move(self,piece,row,col):
        # allows swaping positions for pieces, basically deleting from one spot and appending
        # to where it desires to move
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row,col)
        if row == rows - 1 or row == 0:
            piece.make_king()
            if piece != 0:
                if piece.color == white:
                    self.white_kings += 1
                else:
                    self.red_kings += 1
    
    def get_piece(self,row,col): #give it the row n col, it ill return u a piece
        return self.board[row][col]
    
    def get_valid_moves(self,piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.king or piece.color == red:
            moves.update(self._traverse_left(row-1, max(row-3, -1),-1, piece.color, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1),-1, piece.color, right))
        if piece.king or piece.color == white:
            moves.update(self._traverse_left(row+1, min(row+3, rows),1, piece.color, left))
            moves.update(self._traverse_right(row+1, min(row+3, rows),1, piece.color, right))
        return moves

    def _traverse_left(self,start,stop,step,color,left,skipped=[]):
        moves = {}
        last = []
        for r in range(start,stop,step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last
                else:
                    moves[(r, left)] = skipped + last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, rows)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
        
            left -= 1
        return moves

    def _traverse_right(self,start,stop,step,color,right,skipped=[]):
        moves = {}
        last = []
        for r in range(start,stop,step):
            if right >= cols:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last
                else:
                    moves[(r, right)] = skipped + last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, rows)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves
    
    def remove(self,pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0 and piece.color == white:
                self.white_left -= 1
            else:
                self.red_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return red
        elif self.red_left <= 0:
            return white
        else:
            return None

    def get_all_pieces(self,color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def evaluate(self): #a way to incentivze the ai to make moves keeping the difference between the pieces
        # of its opponent and its own in mind, and seeing the king pieces as advantagious
        return self.white_left - self.red_left + (self.white_kings*0.5 - self.red_kings*0.5)
    