"""
class: Chessboard
"""
import itertools

from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK
from utils import str_repr, nbr_repr


class PieceNotFoundException(Exception):
    def __init__(self, player, position):
        self.player = player
        self.position = position

    def __str__(self):
        return 'no {} found at {}}'


class ImpossibleMoveException(Exception):
    def __init__(self, piece, target):
        self.piece = piece
        self.target = target

    def __str__(self):
        return 'Impossible move: {} {}'.format(self.piece, )


class Chessboard:
    def __init__(self):
        self.squares = {}
        self.blackPieces = []
        self.whitePieces = []

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
        self.blackPieces.append(King('d' + '8', BLACK))
        self.blackPieces.append(Queen('e' + '8', BLACK))
        self.blackPieces.append(Bishop('f' + '8', BLACK))
        self.blackPieces.append(Knight('g' + '8', BLACK))
        self.blackPieces.append(Rook('h' + '8', BLACK))

    def movePiece(self, color, start, target):
        pieces = self.whitePieces if color == WHITE else self.blackPieces
        for p in pieces:
            if p.position == start:
                piece = p
                break
        else:
            raise PieceNotFoundException()
        try:
            self.validateMove(target, piece)
            piece.setPosition(target)
        except Exception as e:
            return str(e)

    def validateMove(self, target, piece):
        possible_moves = piece.possibleMoves()

        if target not in possible_moves:
            raise ImpossibleMoveException(piece, target)

        if self.isTargetBlocked(target, piece):
            raise ImpossibleMoveException(piece, target)

    def isTargetBlocked(self, target, piece):
        if self.isTargetSameColor(target, piece) or self.isTargetObstructed(target, piece):
            return True
        else:
            return False

    def isTargetSameColor(self, target, piece):
        active_color = piece.color
        if active_color == WHITE:
            for passive_piece in self.whitePieces:
                if passive_piece.getPosition() == target:
                    if passive_piece.color == active_color:
                        return True
        else:
            for passive_piece in self.blackPieces:
                if passive_piece.getPosition() == target:
                    if passive_piece.color == active_color:
                        return True
        return False

    def isTargetObstructed(self, target, piece):
        return piece.isObstructed(target, self.whitePieces + self.blackPieces)

    def __str__(self):
        squares = {p.position: p.getName() for p in self.whitePieces + self.blackPieces}
        s = '   A B C D E F G H \n'
        for row in reversed(range(0, 8)):
            s += chr(ord('1') + row) + ' '
            for column in range(0, 8):
                s += ' ' + squares.get((column, row), '#')
            s += '\n'
        return s
