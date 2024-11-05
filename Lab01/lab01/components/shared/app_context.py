from simple_console import AbstractAppContext

from lab01.infrastructure.result_storage import ResultStorage


class AppContext(AbstractAppContext):
    def __init__(self) -> None:
        self._result_storage = ResultStorage()

    @property
    def result_storage(self) -> ResultStorage:
        return self._result_storage
