"""
Program: Chess
av: Olof Svedvall
version 0.3
"""

import sys

from chessboard import Chessboard


class Program():
    def __init__(self):
        self.chessboard = Chessboard()
        self.message = ''

    def play(self):
        while self.message != 'q':
            try:
                self.message = input('>>> ')
                self.chessboard.getMessage(self.message)

            except KeyboardInterrupt:
                print()

            except EOFError:
                print('\nBye!')
                sys.exit()


if __name__ == '__main__':
    program = Program()
    program.play()
