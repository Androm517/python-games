"""
classes: Piece, Pawn, Knight, Rook, Bishop, Queen, King
"""
from utils import str_repr, nbr_repr
from position import Position


BLACK = 'black'
WHITE = 'white'
COLORS = (BLACK, WHITE)


class Piece:
    def __init__(self, position, color):
        if color not in COLORS:
            raise ValueError('{} is not a valid color'.format(color))
        self.color = color
        self.position = Position(position)
        self.firstMove = True

    def getPosition(self):
        return self.position

    def setPosition(self, target):
        self.position = Position(target)
        self.firstMove = False

    def removeMoves(self, possible_moves):
        remove_moves = []
        for move in possible_moves:
            tmp_move = move.coordinates
            if tmp_move[0] < 0 or tmp_move[0] > 8 or tmp_move[1] < 0 or tmp_move[1] > 8:
                remove_moves.append(tmp_move)
        for move in remove_moves:
            possible_moves.remove(move)

    def isAtPosition(self, target):
        if self.position == Position(target):
            return True
        else:
            return False

    def isPossibleMove(self, target):
        if Position(target) in self.possibleMoves():
            return True
        else:
            return False

    def isSameColor(self, target, whitePieces, blackPieces):
        pieces = whitePieces if self.color == WHITE else blackPieces
        for passive_piece in pieces:
            if passive_piece.isAtPosition(target) and passive_piece.color == self.color:
                return True
        return False

    def isObstructed(self, target, whitePieces, blackPieces):
        pieces = whitePieces + blackPieces
        unit_vector = self.unitVector(Position(target))
        pos = self.position
        pos = pos.add(unit_vector)
        while pos != Position(target):
            for piece in pieces:
                if piece.position == pos:
                    return True
            pos = pos.add(unit_vector)
        return False

    # To be overridden by actual pieces
    def getName(self):
        raise NotImplemented()

    def __str__(self):
        return self.getName() + str_repr(self.position)


class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        row, column = self.position.getRow(), self.position.getColumn()
        move_forward = row
        move_left = row.sub(column)
        move_right = row.add(column)
        if self.color == WHITE:
            possible_moves = [self.position.add(move_forward), self.position.add(move_left), self.position.add(move_right)]
            if self.firstMove:
                double = Position((2, 0))
                possible_moves.append(self.position.add(double) )
        else:
            possible_moves = [self.position.sub(move_forward), self.position.sub(move_left), self.position.sub(move_right)]
            if self.firstMove:
                double = Position((2, 0))
                possible_moves.append(self.position.sub(double))
        return possible_moves

    def isObstructed(self, target, whitePieces, blackPieces):
        pieces = whitePieces + blackPieces
        if self.color == WHITE:
            forward = self.position.add(Position( (1, 0) ) )
            double_forward = forward.add(Position( (1, 0) ) )
            left = self.position.add( Position(1, -1))
            right = self.position.add( Position(1, 1))
        else:
            forward = self.position.sub(Position((1, 0)))
            double_forward = forward.sub(Position((1, 0)))
            left = self.position.sub(Position(1, -1))
            right = self.position.sub(Position(1, 1))
        move = Position(target)
        if move == forward:
            for piece in pieces:
                if piece.position == forward:
                    return True
        if move == double_forward:
            for piece in pieces:
                if piece.position == forward:
                    return True
            for piece in pieces:
                if piece.position == double_forward:
                    return True
        if move == left:
            for piece in pieces:
                if piece.position == left:
                    return True
        if move == right:
            for piece in pieces:
                if piece.position == right:
                    return True
        return False

    def getName(self):
        if self.color == BLACK:
            return '\u265F'
        return '\u2659'


class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def isObstructed(self, target, whitePieces, blackPieces):
        pieces = whitePieces + blackPieces
        unit_vector = self.unitVector(Position(target))
        pos = self.position
        pos = pos.add(unit_vector)
        while pos != Position(target):
            for piece in pieces:
                if piece.position == pos:
                    return True
            pos = pos.add(unit_vector)
        return False

    def possibleMoves(self):
        row, column = self.position.getRow(), self.position.getColumn()
        possible_moves = [row.add(Position( (0, k))) for k in range(0, 8)]
        possible_moves.extend([column.add(Position( (k, 0))) for k in range(0, 8)])
        while self.position in possible_moves:
            possible_moves.remove(self.position)
        return possible_moves

    def getName(self):
        if self.color == BLACK:
            return '\u265C'
        return '\u2656'


class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        move_one = Position( (2, 1))
        move_two = Position( (2, -1))
        move_three = Position( (-2, 1))
        move_four = Position( (-2, -1))
        move_five = Position( (2, 1))
        move_six = Position( (2, -1))
        move_seven = Position( (-2, 1))
        move_eight = Position( (-2, -1))
        moves = [move_one, move_two, move_three, move_four, move_five, move_six, move_seven, move_eight]
        possible_moves = [self.position.add(move) for move in moves]
        self.removeMoves(possible_moves)
        return possible_moves

    def isObstructed(self, target, whitePieces, blackPieces):
        return False

    def getName(self):
        if self.color == BLACK:
            return '\u265E'
        return '\u2658'


class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        direction_upper_right = Position( (1, 1))
        direction_down_right = Position( (-1, 1))
        direction_upper_left = Position( (1, -1))
        direction_down_left = Position( (-1, -1))
        possible_moves = [self.position.add(direction_upper_right.multiply(k)) for k in range(8)]
        possible_moves.extend([self.position.add(direction_down_right.multiply(k)) for k in range(8)])
        possible_moves.extend([self.position.add(direction_upper_left.multiply(k)) for k in range(8)])
        possible_moves.extend([self.position.add(direction_down_left.multiply(k)) for k in range(8)])
        while self.position in possible_moves:
            possible_moves.remove(self.position)
        self.removeMoves(possible_moves)
        return possible_moves

    def getName(self):
        if self.color == BLACK:
            return '\u265D'
        return '\u2657'


class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMovesRookMoves(self):
        row, column = self.position.getRow(), self.position.getColumn()
        possible_moves = [row.add(Position((0, k))) for k in range(0, 8)]
        possible_moves.extend([column.add(Position((k, 0))) for k in range(0, 8)])
        while self.position in possible_moves:
            possible_moves.remove(self.position)
        return possible_moves

    def possibleMovesBishopMoves(self):
        direction_upper_right = Position( (1, 1))
        direction_down_right = Position( (-1, 1))
        direction_upper_left = Position( (1, -1))
        direction_down_left = Position( (-1, -1))
        possible_moves = [self.position.add(direction_upper_right.multiply(k)) for k in range(8)]
        possible_moves.extend([self.position.add(direction_down_right.multiply(k)) for k in range(8)])
        possible_moves.extend([self.position.add(direction_upper_left.multiply(k)) for k in range(8)])
        possible_moves.extend([self.position.add(direction_down_left.multiply(k)) for k in range(8)])
        while self.position in possible_moves:
            possible_moves.remove(self.position)
        self.removeMoves(possible_moves)
        return possible_moves

    def possibleMoves(self):
        possible_moves = self.possibleMovesRookMoves()
        possible_moves.extend(self.possibleMovesBishopMoves())
        return possible_moves


    def getName(self):
        if self.color == BLACK:
            return '\u265B'
        return '\u2655'


class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        move_one = Position( (1, -1))
        move_two = Position( (1, 0))
        move_three = Position( (1, 1))
        move_four = Position( (0, 1))
        move_five = Position( (-1, 1))
        move_six = Position( (-1, 0))
        move_seven = Position( (-1, -1))
        move_eight = Position( (0, -1))
        moves = [move_one, move_two, move_three, move_four, move_five, move_six, move_seven, move_eight]
        possible_moves = [self.position.add(move) for move in moves]
        return possible_moves

    def isObstructed(self, target, whitePieces, blackPieces):
        return False

    def getName(self):
        if self.color == BLACK:
            return '\u265A'
        return '\u2654'
