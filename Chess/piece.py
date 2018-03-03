"""
classes: Piece, Pawn, Knight, Rook, Bishop, Queen, King
"""


class Piece:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    # To be overridden by actual pieces
    def getName(self):
        raise NotImplemented()


class Pawn(Piece):
    def __init__(self, position=(1,1), color='#'):
        super().__init__(position, color)

    def possibleMoves(self, move_from):
        i, j = move_from
        possible_moves = [(i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        return possible_moves

    def getName(self):
        if self.color == '+':
            return '\u265F'
        return '\u2659'


class Rook(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(position, color)

    def possibleMoves(self, move_from):
        i, j = move_from
        possible_moves = [(i, k) for k in range(ord('a'), ord('a') + 8)]
        possible_moves.extend([(k, j) for k in range(1, 9)])
        possible_moves.remove((i, j))
        return possible_moves

    def getName(self):
        if self.color == '+':
            return '\u265C'
        return '\u2656'


class Knight(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(position, color)

    def possibleMoves(self, move_from):
        i, j = move_from
        possible_moves = [(i + 2, j + 1), (i + 2, j - 1)]
        possible_moves = [(i - 2, j + 1), (i - 2, j - 1)]
        possible_moves = [(i - 2, j + 1), (i - 2, j - 1)]
        for row in range(i - 8, i + 9):
            possible_moves.append((row, j))
        for column in range(j - 8, i + 9):
            possible_moves.append((i, column))
        return possible_moves

    def getName(self):
        if self.color == '+':
            return '\u265E'
        return '\u2658'


class Bishop(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(position, color)

    def getName(self):
        if self.color == '+':
            return '\u265D'
        return '\u2657'


class Queen(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(position, color)

    def getName(self):
        if self.color == '+':
            return '\u265B'
        return '\u2655'


class King(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(position, color)

    def getName(self):
        if self.color == '+':
            return '\u265A'
        return '\u2654'
