"""
classes: Piece, Pawn, Knight, Rook, Bishop, Queen, King
constants: BLACK, WHITE, COLORS
"""


BLACK = 'black'
WHITE = 'white'
COLORS = (BLACK, WHITE)


class Piece:
    """ Piece is a interface to chess pieces."""
    def __init__(self, position, color, name):
        if color not in COLORS:
            raise ValueError('{} is not a valid color'.format(color))
        self.color = color
        self.position = position
        self.name = name

    # To be overridden by actual pieces
    def getName(self):
        raise NotImplemented()

    def __str__(self):
        return self.getName() + str(self.position)


class Pawn(Piece):
    """ Implements Pawn."""
    def __init__(self, position, color, name):
        super().__init__(position, color, name)

    def getName(self):
        if self.color == BLACK:
            return '\u265F'
        return '\u2659'


class Rook(Piece):
    """ Implements Rook."""
    def __init__(self, position, color, name):
        super().__init__(position, color, name)

    def getName(self):
        if self.color == BLACK:
            return '\u265C'
        return '\u2656'


class Knight(Piece):
    """ Implements Knight."""
    def __init__(self, position, color, name):
        super().__init__(position, color, name)

    def getName(self):
        if self.color == BLACK:
            return '\u265E'
        return '\u2658'


class Bishop(Piece):
    """ Implements Bishop."""
    def __init__(self, position, color, name):
        super().__init__(position, color, name)

    def getName(self):
        if self.color == BLACK:
            return '\u265D'
        return '\u2657'


class Queen(Piece):
    """ Implements Queen."""
    def __init__(self, position, color, name):
        super().__init__(position, color, name)

    def getName(self):
        if self.color == BLACK:
            return '\u265B'
        return '\u2655'


class King(Piece):
    """ Implements King."""
    def __init__(self, position, color, name):
        super().__init__(position, color, name)

    def getName(self):
        if self.color == BLACK:
            return '\u265A'
        return '\u2654'
