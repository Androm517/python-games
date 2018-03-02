"""
classes: Piece, Pawn, Knight, Rook, Bishop, Queen, King
"""

class Piece:
    def __init__(self, name, position, color):
        self.position = position
        self.name = name
        if color is not None:
            self.name = color + self.name[1:]
        self.color = color

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getName(self):
        return self.name


class Pawn(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(' P  ', position, color)

    def possibleMoves(self, move_from):
        i, j = move_from
        possible_moves = [(i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        return possible_moves


class Rook(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(' R  ', position, color)


class Knight(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(' Kn ', position, color)


class Bishop(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(' B  ', position, color)


class Queen(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(' Q  ', position, color)


class King(Piece):
    def __init__(self, position='a1', color='#'):
        super().__init__(' K  ', position, color)
