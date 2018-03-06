"""
class: Chessboard
"""
import logging

from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK
from exceptions import NotYourTurnException, PieceNotFoundException, ImpossibleMoveException


logger = logging.getLogger(__name__)


class Chessboard:
    def __init__(self):
        self.squares = {}
        self.blackPieces = []
        self.whitePieces = []
        self.currentPlayer = WHITE
        self.winner = None

        self.setupInitialPosition()

    def setupInitialPosition(self):
        self.whitePieces += [Pawn(col + '2', WHITE) for col in 'abcdefgh']
        self.whitePieces.append(Rook('a' + '1', WHITE))
        self.whitePieces.append(Knight('b' + '1', WHITE))
        self.whitePieces.append(Bishop('c' + '1', WHITE))
        self.whitePieces.append(Queen('d' + '1', WHITE))
        self.whitePieces.append(King('e' + '1', WHITE))
        self.whitePieces.append(Bishop('f' + '1', WHITE))
        self.whitePieces.append(Knight('g' + '1', WHITE))
        self.whitePieces.append(Rook('h' + '1', WHITE))

        self.blackPieces += [Pawn(col + '7', BLACK) for col in 'abcdefgh']
        self.blackPieces.append(Rook('a' + '8', BLACK))
        self.blackPieces.append(Knight('b' + '8', BLACK))
        self.blackPieces.append(Bishop('c' + '8', BLACK))
        self.blackPieces.append(Queen('d' + '8', BLACK))
        self.blackPieces.append(King('e' + '8', BLACK))
        self.blackPieces.append(Bishop('f' + '8', BLACK))
        self.blackPieces.append(Knight('g' + '8', BLACK))
        self.blackPieces.append(Rook('h' + '8', BLACK))

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
        passive, piece = self.getActivePiece(color, start)
        self.validateMove(piece, target)
        # remove taken pieces (if any)
        for i, p in enumerate(passive):
            if p.isAtPosition(target):
                del passive[i]
                break
        piece.setPosition(target)

    def getActivePiece(self, color, start):
        pieces, passive = (self.whitePieces, self.blackPieces) if color == WHITE else (
        self.blackPieces, self.whitePieces)
        for p in pieces:
            if p.isAtPosition(start):
                piece = p
                break
        else:
            raise PieceNotFoundException(color, start)
        return passive, piece

    def isPositionOnChessboard(self, start):
        if not start[0] in 'abcdefgh' or not start[1] in '12345678':
            return False
        else:
            return True

    def validateMove(self, piece, target):
        if not piece.isPossibleMove(target):
            raise ImpossibleMoveException(piece, target)
        if self.isTargetBlocked(piece, target):
            raise ImpossibleMoveException(piece, target)

    def isTargetBlocked(self, piece, target):
        if self.isTargetSameColor(piece, target) or self.isTargetObstructed(piece, target):
            return True
        else:
            return False

    def isTargetSameColor(self, piece, target):
        return piece.isSameColor(target, self.whitePieces, self.blackPieces)

    def isTargetObstructed(self, piece, target):
        return piece.isObstructed(target, self.whitePieces, self.blackPieces)

    def __str__(self):
        squares = {str(p.getPosition()): p.getName() for p in self.whitePieces + self.blackPieces}
        s = '  A B C D E F G H \n'
        for row in '87654321':
            s += row + ' '
            s += ' '.join(squares.get(column + row, '#') for column in 'abcdefgh')
            s += '\n'
        return s
