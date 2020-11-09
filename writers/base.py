import abc
from typing import Optional


class BaseWriter(metaclass=abc.ABCMeta):

    def __init__(self, location: Optional[str] = None):
        # @PROD- this can be used when wish to write to file (for example)
        # for other resources there might be a need for additional params (such as role to assume for aws resources)
        self._location = location

    def write(self, msg: str) -> None:
        raise NotImplementedError('write')
