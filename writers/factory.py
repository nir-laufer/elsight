from typing import Optional
from writers.base import BaseWriter
from writers.screen import ScreenWriter


class WritersFactory:

    _SCREEN_TYPE = 'screen'

    _WRITES = {
        _SCREEN_TYPE: ScreenWriter
        # @PROD - in a prod scenario there will probably a need to implement more writers- local file, s3, kinsesis, and such
        # Even if some of the writers aren't requested by product definition I would make sure we have the tools we need in
        # order to properly test the feature.
    }

    def create_writer(self, writer_type: str, location: Optional[str] = None) -> BaseWriter:
        writer_type = self._WRITES.get(writer_type)

        if not writer_type:
            raise NotImplementedError(f'There is no writer from type- {writer_type}')

        return writer_type(location)
