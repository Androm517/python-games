"""
class: Chessboard
"""
from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK


class PieceNotFoundException(Exception):
    pass


class ImpossibleMoveException(Exception):
    pass


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
        self.blackPieces.append(Queen('d' + '8', BLACK))
        self.blackPieces.append(King('e' + '8', BLACK))
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
            self.validateMove(piece, target)
            piece.setPosition(target)
        except Exception as e:
            return str(e)

    def validateMove(self, piece, target):
        possible_moves = piece.possibleMoves()
        if target not in possible_moves:
            raise ImpossibleMoveException(target)

    def __str__(self):
        s = '   A B C D E F G H \n'
        for row in '12345678'[-1::-1]:
            s += row + ' '
            for column in 'abcdefgh':
                if row + column in self.squares:
                    s += ' ' + self.squares[row + column].getName()
                else:
                    s += ' #'
            s += '\n'
        return s
