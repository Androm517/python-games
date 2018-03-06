

class ChessException(Exception):
    pass


class UnknownCommand(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return 'Unknown command: {}'.format(self.cmd)


class NotYourTurnException(ChessException):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'not your turn, {}!'.format(self.color)


class PieceNotFoundException(ChessException):
    def __init__(self, player, position):
        self.player = player
        self.position = position

    def __str__(self):
        return 'no {} piece found at {}'.format(self.player, self.position)


class ImpossibleMoveException(ChessException):
    def __init__(self, piece, target):
        self.piece = piece
        self.target = target

    def __str__(self):
        return 'Impossible move: {} {}'.format(self.piece, self.target)
