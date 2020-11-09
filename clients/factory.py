from clients.base import BaseClient
from clients.tcp import TcpClient


class ClientsFactory:

    _TCP_TYPE = 'tcp'

    _CLIENTS = {
        _TCP_TYPE: TcpClient,
    }
    # @PROD- we can add here the different types

    def create_client(self, client_type: str) -> BaseClient:
        client_class = self._CLIENTS.get(client_type)

        if not client_class:
            raise NotImplementedError(f'There is no client from type- {client_type}')

        return client_class()
