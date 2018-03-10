"""
class: Chessboard
"""
import logging

from gameRules import GameRules, WHITE, BLACK, COLORS
from exceptions import NotYourTurnException


logger = logging.getLogger(__name__)


class Chessboard:
    """ Chessboard keeps track what color is at play. It has a set of GameRules to check if a move is correct.
    A position is represented as letter + number ('a1'), because its a chessboard."""
    def __init__(self):
        self.currentPlayer = WHITE
        self.winner = None
        self.gameRules = GameRules()

    def movePiece(self, color, start, target):
        self.checkInputArgs(color, start, target)
        self.makeMove(color, start, target)
        self.currentPlayer = BLACK if self.currentPlayer == WHITE else WHITE

        return "Move OK!"

    def checkInputArgs(self, color, start, target):
        if color != self.currentPlayer:
            raise NotYourTurnException(color)
        if not self.isPositionOnChessboard(start):
            raise ValueError('{} is not a valid position'.format(start))
        if not self.isPositionOnChessboard(target):
            raise ValueError('{} is not a valid position'.format(target))

    def makeMove(self, color, start, target):
        self.gameRules.applyGameRules(color, start, target)

    def isPositionOnChessboard(self, start):
        if start[0] in 'abcdefgh' and start[1] in '12345678':
            return True
        else:
            return False

    def __str__(self):
        return str(self.gameRules)
