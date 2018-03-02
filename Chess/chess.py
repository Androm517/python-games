"""
Program: Chess
av: Olof Svedvall
version 0.3
"""
from chessboard import Chessboard

class Program():
    def __init__(self):
        self.chessboard = Chessboard()
        self.message = ''

    def play(self):
        while self.message != 'q':
            self.message = input('>>> ')
            self.chessboard.getMessage(self.message)


if __name__ == '__main__':
    program = Program()
    program.play()
