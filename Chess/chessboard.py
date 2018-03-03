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

    def validateMove(self, target, piece):
        possible_moves = piece.possibleMoves()
        if target not in possible_moves:
            raise ImpossibleMoveException(target)
        if self.isTargetBlocked(target, piece):
            raise ImpossibleMoveException(target)

    def isTargetBlocked(self, target, piece):
        if self.isTargetSameColor(target, piece) or self.isTargetObstructed(target, piece):
            return True
        else:
            return False

    def isTargetSameColor(self, target, piece):
        active_color = piece.color
        target_color = None
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
        s = '   A B C D E F G H \n'
        pieces = self.whitePieces + self.blackPieces
        for row in range(0,8):
            s += str(row) + ' '
            for column in range(0,8):
                for piece in pieces:
                    if (row, column) == piece.getPosition():
                        s += ' ' + piece.getName()
                        break
                else:
                    s += ' #'
            s += '\n'
        return s
