import socket
import threading
import logging

from chessboard import Chessboard

BIND_IP = '0.0.0.0'
BIND_PORT = 9999


class Server:
    def __init__(self):
        self.players = []
        self.boardLock = threading.Lock()
        self.board = Chessboard()

    # start server and stuff... as someone connects add a player to the list of players
    def run(self):
        sockets = []

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((BIND_IP, BIND_PORT))
        server.listen(5)  # max backlog of connections

        print('Listening on {}:{}'.format(BIND_IP, BIND_PORT))

        def handle_client_connection(client_socket):
            while True:
                try:
                    message = client_socket.recv(4096).decode('utf-8')
                    if not message:
                        break
                    with self.boardLock:
                        response = self.board.getMessage(message)
                    client_socket.send(bytes(str(response), 'utf-8'))

                except Exception as e:
                    logging.exception(e)

        while True:
            try:
                client_sock, address = server.accept()
                print('Accepted connection from {}:{}'.format(address[0], address[1]))
                sockets.append(client_sock)
                client_handler = threading.Thread(
                    target=handle_client_connection,
                    args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
                )
                client_handler.daemon = True
                client_handler.start()

            except KeyboardInterrupt:
                break

        for s in sockets:
            s.close()
            break

        server.close()


if __name__ == '__main__':
    Server().run()
