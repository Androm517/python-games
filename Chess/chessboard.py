"""
class: Chessboard
"""
import logging

from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK
from gameRules import GameRules
from exceptions import NotYourTurnException, PieceNotFoundException, ImpossibleMoveException


logger = logging.getLogger(__name__)


class Chessboard:
    def __init__(self):
        self.squares = {}
        self.black_pieces = []
        self.white_pieces = []
        self.currentPlayer = WHITE
        self.winner = None
        self.setupInitialPosition()
        self.gameRules = GameRules(self.white_pieces, self.black_pieces)

    def setupInitialPosition(self):
        self.white_pieces += [Pawn(col + '2', WHITE, 'pawn') for col in 'abcdefgh']
        self.white_pieces.append(Rook('a' + '1', WHITE, 'rook'))
        self.white_pieces.append(Knight('b' + '1', WHITE, 'knight'))
        self.white_pieces.append(Bishop('c' + '1', WHITE, 'bishop'))
        self.white_pieces.append(Queen('d' + '1', WHITE, 'queen'))
        self.white_pieces.append(King('e' + '1', WHITE, 'king'))
        self.white_pieces.append(Bishop('f' + '1', WHITE, 'bishop'))
        self.white_pieces.append(Knight('g' + '1', WHITE, 'knight'))
        self.white_pieces.append(Rook('h' + '1', WHITE, 'rook'))

        self.black_pieces += [Pawn(col + '7', BLACK, 'pawn') for col in 'abcdefgh']
        self.black_pieces.append(Rook('a' + '8', BLACK, 'rook'))
        self.black_pieces.append(Knight('b' + '8', BLACK, 'knight'))
        self.black_pieces.append(Bishop('c' + '8', BLACK, 'bishop'))
        self.black_pieces.append(Queen('d' + '8', BLACK, 'queen'))
        self.black_pieces.append(King('e' + '8', BLACK, 'king'))
        self.black_pieces.append(Bishop('f' + '8', BLACK, 'bishop'))
        self.black_pieces.append(Knight('g' + '8', BLACK, 'knight'))
        self.black_pieces.append(Rook('h' + '8', BLACK, 'rook'))

    def movePiece(self, color, start, target):
        self.checkInputArgs(color, start, target)
        self.makeMove(color, start, target)
        self.currentPlayer = BLACK if self.currentPlayer == WHITE else WHITE

        return "Move OK!"

    def checkInputArgs(self, color, start, target):
        if color != self.currentPlayer:
            raise NotYourTurnException(color)
        if not self.isPositionOnChessboard(start):
            raise ValueError('{} is not a valid position'.format(start))
        if not self.isPositionOnChessboard(target):
            raise ValueError('{} is not a valid position'.format(target))

    def makeMove(self, color, start, target):
        active_piece, passive_pieces = self.getActivePieceAndPassivePieces(color, start)
        self.gameRules.applyGameRules(active_piece, target)
        for piece in passive_pieces:
            if piece.isAtPosition(target):
                passive_pieces.remove(piece)
        active_piece.setPosition(target)

    def isPositionOnChessboard(self, start):
        if not start[0] in 'abcdefgh' or not start[1] in '12345678':
            return False
        else:
            return True

    def getActivePieceAndPassivePieces(self, color, start):
        active_pieces, passive_pieces = (self.white_pieces, self.black_pieces) if color == WHITE else (
            self.black_pieces, self.white_pieces)
        for active_piece in active_pieces:
            if active_piece.isAtPosition(start):
                piece = active_piece
                break
        else:
            raise PieceNotFoundException(color, start)
        return piece, passive_pieces

    def validateMove(self, piece, target):
        if not piece.isPossibleMove(target):
            raise ImpossibleMoveException(piece, target)
        if self.isTargetBlocked(piece, target):
            raise ImpossibleMoveException(piece, target)

    def removeCapturedPiece(self, passive_pieces, target):
        for i, passive_piece in enumerate(passive_pieces):
            if passive_piece.isAtPosition(target):
                del passive_pieces[i]
                break

    def isTargetBlocked(self, piece, target):
        if self.isTargetSameColor(piece, target) or self.isTargetObstructed(piece, target):
            return True
        else:
            return False

    def isTargetSameColor(self, piece, target):
        return piece.isSameColor(target, self.white_pieces, self.black_pieces)

    def isTargetObstructed(self, piece, target):
        return piece.isObstructed(target, self.white_pieces, self.black_pieces)

    def __str__(self):
        squares = {str(p.getPosition()): p.getName() for p in self.white_pieces + self.black_pieces}
        s = '  A B C D E F G H \n'
        for row in '87654321':
            s += row + ' '
            s += ' '.join(squares.get(column + row, '#') for column in 'abcdefgh')
            s += '\n'
        return s
