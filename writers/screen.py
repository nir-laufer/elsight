from writers.base import BaseWriter


class ScreenWriter(BaseWriter):

    def write(self, msg: str) -> None:
        print(msg)
