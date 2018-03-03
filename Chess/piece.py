"""
classes: Piece, Pawn, Knight, Rook, Bishop, Queen, King
"""


BLACK = 'black'
WHITE = 'white'
COLORS = (BLACK, WHITE)


class Piece:
    def __init__(self, position, color):
        if color not in COLORS:
            raise ValueError('{} is not a valid color'.format(color))
        self.color = color

        if isinstance(position, str):
            if len(position) != 2:
                raise ValueError('{} is not a valid position'.format(position))
            position = (ord(position[0]) - ord('a'), ord(position[1]) - ord('1'))
        if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
            raise ValueError('{} is not a valid position'.format(position))

        self.position = position

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    # To be overridden by actual pieces
    def getName(self):
        raise NotImplemented()


class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        i, j = self.position
        possible_moves = [(i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        return possible_moves

    def getName(self):
        if self.color == WHITE:
            return '\u265F'
        return '\u2659'


class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        i, j = self.position
        possible_moves = [(i, k) for k in range(0, 8)]
        possible_moves.extend([(k, j) for k in range(0, 8)])
        possible_moves.remove((i, j))
        return possible_moves

    def getName(self):
        if self.color == WHITE:
            return '\u265C'
        return '\u2656'


class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        i, j = self.position
        possible_moves = [(i + k, j - 1) for k in range(-2, 3, 4)]
        possible_moves = [(i + k, j + 1) for k in range(-2, 3, 4)]
        possible_moves = [(i + 1, j + k) for k in range(-2, 3, 4)]
        possible_moves = [(i - 1, j + k) for k in range(-2, 3, 4)]
        remove_moves = []
        for move in possible_moves:
            if move[0] < 0 or move[0] > 8 or move[1] < 0 or move[1] > 8:
                remove_moves.append(move)
        for move in remove_moves:
            possible_moves.remove(move)
        return possible_moves

    def getName(self):
        if self.color == WHITE:
            return '\u265E'
        return '\u2658'


class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def possibleMoves(self):
        i, j = self.position
        possible_moves = [(i + k, j - 1) for k in range(-2, 3, 4)]
        possible_moves.extend([(i + k, j + 1) for k in range(-2, 3, 4)])
        possible_moves.extend([(i + 1, j + k) for k in range(-2, 3, 4)])
        possible_moves.extend([(i - 1, j + k) for k in range(-2, 3, 4)])
        remove_moves = []
        for move in possible_moves:
            if move[0] < 0 or move[0] > 8 or move[1] < 0 or move[1] > 8:
                remove_moves.append(move)
        for move in remove_moves:
            possible_moves.remove(move)
        return possible_moves

    def getName(self):
        if self.color == WHITE:
            return '\u265D'
        return '\u2657'


class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def getName(self):
        if self.color == WHITE:
            return '\u265B'
        return '\u2655'


class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)

    def getName(self):
        if self.color == WHITE:
            return '\u265A'
        return '\u2654'
