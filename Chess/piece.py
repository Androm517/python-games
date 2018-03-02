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
    def __init__(self, position='a1', color='#'):
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

    def getName(self):
        if self.color == '+':
            return '\u265C'
        return '\u2656'


class Knight(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(position, color)

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
