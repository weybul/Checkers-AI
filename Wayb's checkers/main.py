import pygame
from checkers.constants import width, height, square_size, white
# from checkers.board import Board
from checkers.game import Game
from algorithm.minimax import minimax
from checkers.pieces import Piece

FPS = 60
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("WAyb's Checkers")


def get_row_col_with_mouse(pos):
    x,y = pos
    row = y // square_size
    col = x // square_size
    return row,col

# main function loop
def main():
    run = True
    clock = pygame.time.Clock() #makes sure that the game runs at a consistent rate
    # board = Board()
    # piece = board.get_piece(0,3)
    # board.move(piece, 3,4)
    game = Game(window)


    while run:
        clock.tick(60)

        if game.turn == white:
            value, nother_board = minimax(game.get_board(), 3, white, game)
            game.ai_move(nother_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row,col = get_row_col_with_mouse(pos)
                game.select(row,col)

        game.update()

    pygame.quit()    

main()
