import pygame
from copy import deepcopy
from checkers.constants import dark_purple, dark_blue, dark_green

red = (255,0,0)
white = (255,255,255)
shiny_dark_red = (139, 0, 0)

def minimax(position,depth,max_player,game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position #if the depth reaches zero return the evaluate pos along with pos
    
    if max_player:
        max_eval = float("-inf")
        best_move = None
        for move in get_all_moves(position,white,game):
            evaluation = minimax(move,depth-1,False,game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    
    else:
        min_eval = float("inf")
        best_move = None
        for move in get_all_moves(position,red,game):
            evaluation = minimax(move,depth-1,True,game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move

def simulated_move(piece,move,board,game,skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board,color,game):
    moves = []
    # the purpose of this func is to get all the possible moves for pieces of a certain color
    # it works by first gettin all the pieces of a certain color
    # and then uses board.get_valid_moves to consider all of the valid moves

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move,skip in valid_moves.items():
            draw_simulated_move(piece,board,game)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row,piece.col)
            nother_board = simulated_move(temp_piece,move,temp_board,game,skip)
            moves.append(nother_board)
    return moves

def draw_simulated_move(piece,board,game):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.window)
    pygame.draw.circle(game.window, dark_purple, (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(0.30)