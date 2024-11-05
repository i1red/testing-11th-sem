from simple_console import display_message
from simple_console import RunItem, RUN_END
from simple_console import AbstractComponent
from simple_console import InputField

from lab01.components.shared.app_context import AppContext
from lab01.core.result import Result
from lab01.utility.parsers import parse_bool
from lab01.components.update_last_result_component import UpdateLastResultComponent
from lab01.components.upsert_result_component import UpsertResultComponent


class PersistResultComponent(AbstractComponent[AppContext]):
    persist_field: InputField[bool]

    def declare_fields(self) -> None:
        self.persist_field = InputField(
            prompt="Записати результати у файл? (Так/Ні):",
            parser=parse_bool(truthy="Так", falsy="Ні")
        )

    def run(self, result: Result) -> RunItem:
        persist = self.persist_field.get_input()

        if not persist:
            display_message("Дані у файл не записано")
            return RUN_END

        if self.context.result_storage.file_count > 0:
            return UpdateLastResultComponent().run(result)

        return UpsertResultComponent().run(result)
