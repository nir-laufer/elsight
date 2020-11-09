import abc


class BaseClient(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def connect(self, server: str, port: int) -> None:
        raise NotImplementedError('connect')

    @abc.abstractmethod
    def send(self, msg: bytes) -> None:
        raise NotImplementedError('send')
