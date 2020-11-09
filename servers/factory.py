from servers.base import BaseServer
from servers.tcp import TcpServer


class ServersFactory:

    _TCP_TYPE = 'tcp'

    _SERVERS = {
        _TCP_TYPE: TcpServer,
    }

    def create_server(self, server_type: str) -> BaseServer:
        server_class = self._SERVERS.get(server_type)

        if not server_class:
            raise NotImplementedError(f'There is no server from type- {server_type}')

        return server_class()