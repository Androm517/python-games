import socket
import threading
import logging
import random

from chessboard import Chessboard
from piece import BLACK, WHITE, COLORS
from player import Player

BIND_IP = '0.0.0.0'
BIND_PORT = 9999


class UnknownCommand(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return 'Unknown command: {}'.format(self.cmd)


class Server:
    def __init__(self):
        self.players = []
        self.boardLock = threading.Lock()
        self.board = Chessboard()
        self.started = False

        self.commands = {
            'move': self.makeMove,
            'surrender': self.give_up,
            'yield': self.give_up,
            'castle': self.castle,
            'say': self.say,
            'print': lambda p: str(self.board)
        }

    def makeMove(self, player, at, to):
        at = (ord(at[0]) - ord('a'), ord(at[1]) - ord('1'))
        to = (ord(to[0]) - ord('a'), ord(to[1]) - ord('1'))
        self.board.movePiece(player.color, at, to)
        return self.board

    def give_up(self, player):
        raise NotImplemented()

    def castle(self, player, where):
        raise NotImplemented()

    def say(self, player, *msg):
        raise NotImplemented()

    def handle_message(self, player, message):
        try:
            with self.boardLock:
                response = self.execute_command(player, *message.split())
        except Exception as e:
            logging.exception(e)
            response = e
        return str(response)

    def execute_command(self, player, *args):
        if not args:
            raise RuntimeError('no args provided...')

        command = args[0]

        if len(command) > 1:
            params = args[1:]
        else:
            params = ()     # empty tuple

        f = self.commands.get(command.lower())
        if not f:
            raise UnknownCommand(command)

        return f(player, *params)

    # start server and stuff... as someone connects add a player to the list of players
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((BIND_IP, BIND_PORT))
        server.listen(5)  # max backlog of connections

        print('Listening on {}:{}'.format(BIND_IP, BIND_PORT))

        while True:
            try:
                client_sock, address = server.accept()
                print('Accepted connection from {}:{}'.format(address[0], address[1]))

                if len(self.players) == 2:
                    client_sock.close()
                    continue

                def handle_client_connection(player):
                    while True:
                        try:
                            message = player.socket.recv(4096).decode('utf-8')
                            if not message:
                                break
                            response = self.handle_message(player, message)
                            player.tell(response)

                        except Exception as e:
                            logging.exception(e)

                if self.players:
                    player = Player(WHITE if self.players[0].color == BLACK else BLACK, client_sock)
                    self.players[0].tell('another player connected, the game can start!')
                else:
                    player = Player(random.choice(COLORS), client_sock)
                player.tell('Welcome to the game! You are {}.'.format(player.color))
                self.players.append(player)

                client_handler = threading.Thread(
                    target=handle_client_connection,
                    args=(player,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
                )
                client_handler.daemon = True
                client_handler.start()

                if len(self.players) == 2:
                    self.game_started = True

            except KeyboardInterrupt:
                break

        for p in self.players:
            p.disconnect()

        server.close()


if __name__ == '__main__':
    Server().run()
