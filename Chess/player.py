import piece
import threading


class Player:
    def __init__(self, color, socket):
        self.socket = socket
        if color not in piece.COLORS:
            raise ValueError('{} is not a valid color'.format(color))
        self.color = color
        self.name = color
        self.socket_lock = threading.Lock()

    def tell(self, message):
        with self.socket_lock:
            self.socket.send(bytes('\r' + message + '\n' + self.color + ': ', 'utf-8'))

    def disconnect(self):
        with self.socket_lock:
            self.socket.send('you have been disconnected from game...')
        self.socket.close()
