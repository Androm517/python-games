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

    def print(self, message):
        if message == 'print':
            s = '\t\t A\t\t B\t\t C\t\t D\t\t E\t\t F\t\t G\t\t H \n'
            for row in '12345678'[-1::-1]:
                s += row + '\t\t'
                for column in 'abcdefgh':
                    if row + column in self.squares:
                        s += self.squares[row + column].getName() + '\t'
                    else:
                        s += '####\t'
                s += '\n'
            print(s)
