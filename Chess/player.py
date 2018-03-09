import piece
import threading
import logging

from exceptions import UnknownCommand


class Player(threading.Thread):
    """ Player connects to the server and is given a color. A player can play the chess pieces that
    corresponds to its color."""
    def __init__(self, color, socket):
        super(Player, self).__init__()

        self.socket = socket
        if color not in piece.COLORS:
            raise ValueError('{} is not a valid color'.format(color))
        self.color = color
        self.name = color
        self.socket_lock = threading.Lock()
        self.commands = {}
        self.opponent = None
        self.daemon = True

    def tell(self, message):
        with self.socket_lock:
            self.socket.send(bytes('\r' + message + '\n' + self.color + ': ', 'utf-8'))

    def disconnect(self):
        with self.socket_lock:
            self.socket.send(bytes('you have been disconnected from game...', 'utf-8'))
        self.socket.close()

    def run(self):
        while True:
            try:
                message = self.socket.recv(4096).decode('utf-8')
                if not message:
                    break
                response = self.handle_message(message)
                if response != 'None':
                    self.tell(response)

            except Exception as e:
                logging.exception(e)

    def handle_message(self, message):
        try:
            response = self.execute_command(*message.split())
        except Exception as e:
            response = e
        return str(response)

    def execute_command(self, *args):
        if not args:
            raise RuntimeError('no args provided...')

        command = args[0]

        if len(args) > 1:
            params = args[1:]
        else:
            params = ()     # empty tuple

        f = self.commands.get(command.lower())
        if not f:
            raise UnknownCommand(command)

        return f(self, *params)
