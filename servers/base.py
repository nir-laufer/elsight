import abc


class BaseServer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare_for_msg(self, host: str, port: int):
        raise NotImplementedError('bind_and_listen')

    @abc.abstractmethod
    def wait_for_new_data(self, time_to_wait_in_secs: int) -> bytes:
        raise NotImplementedError('wait_for_new_data')
