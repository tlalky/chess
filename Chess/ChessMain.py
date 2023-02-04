"""
this file will be responsible for handling user input and displaying current gamestate object.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512  # size of chess board
DIMENSION = 8  # dimensions of chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION  # square size
MAX_FPS = 15  # for animation later on
IMAGES = {}


def loadImages():  # load images only one to be more efficient
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():  # handle user input and update the graphics
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # variable to check if move has been made
    loadImages()  # only do this once before while loop
    running = True
    sqSelected = ()  # no square is selected at start # keep track of user last click -> tuple (row, column)
    playerClicks = []  # keep track of user clicks -> two tuples [(6,4), (3,5)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # mouse handler
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # user clicked same square more than once
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append 1st and 2nd clicks
                if len(playerClicks) == 2:  # if player clicked two different squares meaning to move piece
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    #print(move.getChessNotation())  # for debugging
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []  # reset user clicks
                    else:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo move when "z" is pressed
                    gs.undoMove()
                    moveMade = True  # generate new set of legal moves

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):  # draw squares and pieces on the board
    drawBoard(screen)  # draw squares on board
    drawPieces(screen, gs.board)  # draw pieces on top of the squares


def drawBoard(screen):  # draw squares on the board # top left square is always white
    colors = [p.Color("white"), p.Color("gray")]  # adjusting colors of chess board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):  # draw pieces on top of squares
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()



