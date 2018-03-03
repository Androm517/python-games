"""
class: Chessboard
"""
import itertools

from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK
from utils import str_repr, nbr_repr


class NotYourTurnException(Exception):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'not your turn, {}!'.format(self.color)


class PieceNotFoundException(Exception):
    def __init__(self, player, position):
        self.player = player
        self.position = position

    def __str__(self):
        return 'no {} piece found at {}'.format(self.player, str_repr(self.position))


class ImpossibleMoveException(Exception):
    def __init__(self, piece, target):
        self.piece = piece
        self.target = target

    def __str__(self):
        return 'Impossible move: {} {}'.format(self.piece, str_repr(self.target))


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
        self.blackPieces.append(King('e' + '8', BLACK))
        self.blackPieces.append(Queen('d' + '8', BLACK))
        self.blackPieces.append(Bishop('f' + '8', BLACK))
        self.blackPieces.append(Knight('g' + '8', BLACK))
        self.blackPieces.append(Rook('h' + '8', BLACK))

    def movePiece(self, color, start, target):
        if color != self.currentPlayer:
            raise NotYourTurnException(color)

        pieces, passive = (self.whitePieces, self.blackPieces) if color == WHITE else (self.blackPieces, self.whitePieces)

        for p in pieces:
            if p.position == start:
                piece = p
                break
        else:
            raise PieceNotFoundException()

        try:
            self.validateMove(target, piece)
            # remove taken pieces (if any)
            for p, i in enumerate(passive):
                if p.position == target:
                    passive.pop(i)
                    break
            piece.setPosition(target)
            self.currentPlayer = BLACK if self.currentPlayer == WHITE else BLACK
        except Exception as e:
            return str(e)

        return "Move OK!"

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
        pieces = self.whitePieces if active_color == WHITE else self.blackPieces
        for passive_piece in pieces:
            if passive_piece.getPosition() == target and passive_piece.color == active_color:
                return True
        return False

    def isTargetObstructed(self, target, piece):
        return piece.isObstructed(target, self.whitePieces + self.blackPieces)

    def __str__(self):
        squares = {p.position: p.getName() for p in self.whitePieces + self.blackPieces}
        s = '  A B C D E F G H \n'
        for row in reversed(range(0, 8)):
            s += chr(ord('1') + row) + ' '
            s += ' '.join(squares.get((row, column), '#') for column in range(0, 8))
            s += '\n'
        return s
