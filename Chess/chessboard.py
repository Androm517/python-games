"""
class: Chessboard
"""
import logging

from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK
from position import Position
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
        if color != self.currentPlayer:
            raise NotYourTurnException(color)

        position = Position(start)
        if position.coordinates[0] > 7 or position.coordinates[0] < 0 or position.coordinates[1] > 7 or position.coordinates[1] < 0:
            raise ValueError('{} is not a valid position'.format(position))

        position = Position(target)
        if position.coordinates[0] > 7 or position.coordinates[0] < 0 or position.coordinates[1] > 7 or position.coordinates[1] < 0:
            raise ValueError('{} is not a valid position'.format(position))

        pieces, passive = (self.whitePieces, self.blackPieces) if color == WHITE else (self.blackPieces, self.whitePieces)

        for p in pieces:
            if p.isAtPosition(start):
                piece = p
                break
        else:
            raise PieceNotFoundException(color, start)

        self.validateMove(target, piece)
        # remove taken pieces (if any)
        for i, p in enumerate(passive):
            if p.isAtPosition(target):
                del passive[i]
                break

        piece.setPosition(target)
        self.currentPlayer = BLACK if self.currentPlayer == WHITE else WHITE

        return "Move OK!"

    def validateMove(self, target, piece):
        if not piece.isPossibleMove(target):
            raise ImpossibleMoveException(piece, target)

        if self.isTargetBlocked(target, piece):
            raise ImpossibleMoveException(piece, target)

    def isTargetBlocked(self, target, piece):
        if self.isTargetSameColor(target, piece) or self.isTargetObstructed(target, piece):
            return True
        else:
            return False

    def isTargetSameColor(self, target, piece):
        return piece.isSameColor(target, self.whitePieces, self.blackPieces)

    def isTargetObstructed(self, target, piece):
        return piece.isObstructed(target, self.whitePieces, self.blackPieces)

    def __str__(self):
        squares = {p.position.coordinates: p.getName() for p in self.whitePieces + self.blackPieces}
        s = '  A B C D E F G H \n'
        for row in reversed(range(0, 8)):
            s += chr(ord('1') + row) + ' '
            s += ' '.join(squares.get((row, column), '#') for column in range(0, 8))
            s += '\n'
        return s
