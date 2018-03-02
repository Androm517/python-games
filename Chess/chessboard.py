"""
class: Chessboard
"""
from piece import Pawn, Rook, Knight, Bishop, Queen, King


class Chessboard:
    def __init__(self):
        self.squares = {}
        for row in '12345678':
            if row in '12':
                color ='+'
            else:
                color = '-'
            for column in 'abcdefgh':
                if row in '27':
                    self.squares[row + column] = Pawn(row + column, color)
                elif row in '18' and column in 'ah':
                    self.squares[row + column] = Rook(row + column, color)
                elif row in '18' and column in 'bg':
                    self.squares[row + column] = Knight(row + column, color)
                elif row in '18' and column in 'cf':
                    self.squares[row + column] = Bishop(row + column, color)
                elif row in '18' and column in 'd':
                    self.squares[row + column] = Queen(row + column, color)
                elif row in '18' and column in 'e':
                    self.squares[row + column] = King(row + column, color)

    def getMessage(self, message):
        self.movePiece(message)
        self.print(message)

    def movePiece(self, message):
        print(message)
        move_from, move_to = self.parseMoveMessage(message)
        if move_from is not None:
            chess_piece = self.squares[move_from]
            del self.squares[move_from]
            self.squares[move_to] = chess_piece

    def parseMoveMessage(self, message):
        if ' ' in message:
            move_from, move_to = message.split(' ')
            return move_from[-1::-1], move_to[-1::-1]
        return None, None

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

    def print(self, message):
        if message == 'print':
            print(self)
