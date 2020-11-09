from clients.base import BaseClient
import socket


class TcpClient(BaseClient):

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self._socket.close()

    def connect(self, server: str, port: int) -> None:
        self._socket.connect((server, port))

    def send(self, msg: bytes) -> None:
        self._socket.send(msg)
