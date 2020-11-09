import socket
from servers.base import BaseServer
import time
from typing import Optional


class TcpServer(BaseServer):

    _MAX_BUFFER_SIZE = 1024
    _TIME_TO_WAIT_BETWEEN_CALLS_IN_SECONDS = 0.1

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def prepare_for_msg(self, host: str, port: int) -> None:
        self._socket.bind((host, port))
        self._socket.listen()

    def wait_for_new_data(self, time_to_wait_in_secs: int) -> Optional[bytes]:
        start_time = time.time()
        conn, _ = self._socket.accept()

        with conn:
            while time.time() - start_time < time_to_wait_in_secs:
                time.sleep(self._TIME_TO_WAIT_BETWEEN_CALLS_IN_SECONDS)
                data = conn.recv(self._MAX_BUFFER_SIZE)
                if data:
                    return data
