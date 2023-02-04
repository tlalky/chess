"""
this file is responsible for storing current information of chess game and checking if a move is valid at the current
state. It will also keep a move log.
"""


class GameState():
    def __init__(self):
        # board is 8x8 2d list, each element has 2 characters ( color and piece representation )
        # "--" represents empty space on chess board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whitetomove = True
        self.movelog = []
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):  # take a move as parameter and executes it ( it will not work for en passant, promotion
        self.board[move.startRow][move.startCol] = "--"  # and castling
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)  # log move so we can undo it later or keep the logs of moves
        self.whitetomove = not self.whitetomove  # switch turns
        # update kings position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.movelog) != 0:  # there is at least one move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whitetomove = not self.whitetomove  # switch turn back
            # update kings position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()  # generate all possible moves
        for i in range(len(moves) - 1, -1, -1):  # when removing from list go backwards through that list
            self.makeMove(moves[i])  # for each move make move
            self.whitetomove = not self.whitetomove
            if self.inCheck():
                moves.remove(moves[i])  # if they attack your king it's not a valid move
            self.whitetomove = not self.whitetomove
            self.undoMove()
        if len(moves) == 0:  # either checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves

    def inCheck(self):  # determine if current player is in check
        if self.whitetomove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):  # determine if enemy can attack square r,c
        self.whitetomove = not self.whitetomove  # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()  # generate all opponent moves
        self.whitetomove = not self.whitetomove  # switch turn back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True  # if square is under attack return True
        return False  # else return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                turn = self.board[r][c][0]  # first character of the piece on board ( "w", "b" or "-" )
                if (turn == "w" and self.whitetomove) or (turn == "b" and not self.whitetomove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # call appropriate move function for piece type
        return moves

    def getPawnMoves(self, r, c, moves):  # get all pawn moves for pawn located at (row,col) and add them to move list
        if self.whitetomove:  # white pawns
            if self.board[r - 1][c] == "--":  # one square forward is empty
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # pawn on starting square and two sqaures in fron are empty
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # prevent from going over the board on left side # capture to the left
                if self.board[r - 1][c - 1][0] == "b":  # check if there is black piece on square you want to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # prevent from going over the board on right side # capture to the right
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawns
            if self.board[r + 1][c] == "--":  # one square forward is empty
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # pawn on starting square and two sqaures in fron are empty
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # prevent from going over the board on left side # capture to the left
                if self.board[r + 1][c - 1][0] == "w":  # check if there is white piece on square you want to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # prevent from going over the board on right side # capture to the right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):  # get all rook moves for rook located at (row,col) and add them to move list
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # all possible directions to move at
        if self.whitetomove:  # determine what color are you and what color you can attack
            enemycolor = "b"
        else:
            enemycolor = "w"

        for d in directions:  # loop through all of directions
            for i in range(1, 8):  # test for up to 7 positions if it is empty square in the direction
                endRow = r + d[0] * i  # startRow + (-1 , 0 or 1 ) from directions tuple * 1,2,3,...
                endCol = c + d[1] * i  # startCol + (-1 , 0 or 1 ) from directions tuple * 1,2,3,...
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on the board
                    endPiece = self.board[endRow][endCol]  # assign coordinates to variables
                    if endPiece == "--":  # empty space -> valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))  # append to list of valid moves
                    elif endPiece[0] == enemycolor:  # enemy piece -> valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))  # append to list of valid moves
                        break  # you can't go any further in this direction -> break out of for loop
                    else:  # your piece -> you can't capture your own pieces -> invalid move
                        break
                else:  # not on the board
                    break

    def getKnightMoves(self, r, c, moves):  # get all knig moves for rook located at (row,col) and add them to move list
        directions = ((-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2))  # all possible moves
        if self.whitetomove:
            allycolor = "w"
        else:
            allycolor = "b"

        for d in directions:  # loop through directions tuple
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on the board
                endPiece = self.board[endRow][endCol]  # assign coordinates to variables
                if endPiece[0] != allycolor:  # knight can jump anywhere except on its own pieces
                    moves.append(Move((r, c), (endRow, endCol), self.board))  # not ally piece -> empty or enemy

    def getBishopMoves(self, r, c, moves):  # get all bish moves for rook located at (row,col) and add them to move list
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # all possible directions to move at
        if self.whitetomove:  # determine enemy color
            enemycolor = "b"
        else:
            enemycolor = "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i  # startRow + (-1 or 1 ) from directions tuple * 1,2,3,...
                endCol = c + d[1] * i  # startCol + (-1 or 1 ) from directions tuple * 1,2,3,...
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on the board
                    endPiece = self.board[endRow][endCol]  # assign coordinates to variables
                    if endPiece == "--":  # empty space -> valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))  # append to list of valid moves
                    elif endPiece[0] == enemycolor:  # enemy piece -> valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))  # append to list of valid moves
                        break  # you can't go any further in this direction -> break out of for loop
                    else:  # your piece -> you can't capture your own pieces -> invalid move
                        break
                else:  # not on the board
                    break

    def getQueenMoves(self, r, c, moves):  # get all queen moves for rook located at (row,col) and add them to move list
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):  # get all king moves for rook located at (row,col) and add them to move list
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        if self.whitetomove:  # determine enemy color
            allycolor = "w"
        else:
            allycolor = "b"

        for i in range(8):  # loop through directions tuple
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on the board
                endPiece = self.board[endRow][endCol]  # assign coordinates to variables
                if endPiece[0] != allycolor:  # knight can jump anywhere except on its own pieces
                    moves.append(Move((r, c), (endRow, endCol), self.board))  # not ally piece -> empty or enemy

class Move():
    # maps key to values # key : value                  # changing computer notation to nice chess notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):  # overriding equals method
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
