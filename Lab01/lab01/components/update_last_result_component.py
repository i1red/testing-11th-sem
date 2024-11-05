from simple_console import RunItem, RUN_END
from simple_console import AbstractComponent
from simple_console import InputField

from lab01.components.upsert_result_component import UpsertResultComponent
from lab01.components.update_existing_result_component import UpdateExistingResultComponent
from lab01.components.shared.app_context import AppContext
from lab01.core.result import Result
from lab01.utility.parsers import parse_bool


class UpdateLastResultComponent(AbstractComponent[AppContext]):
    write_to_last_used_file_field: InputField[bool]

    def declare_fields(self) -> None:
        last_file = self.context.result_storage.last_used_file

        self.write_to_last_used_file_field = InputField(
            prompt=f"Записати результати у файл '{last_file}'? (Так/Ні): ",
            parser=parse_bool(truthy="Так", falsy="Ні")
        )

    def run(self, result: Result) -> RunItem:
        write_to_last_used_file = self.write_to_last_used_file_field.get_input()
        result_storage = self.context.result_storage

        if write_to_last_used_file:
            last_file = result_storage.last_used_file
            result_storage.write_result(last_file, result)
            return RUN_END

        if result_storage.file_count == 5:
            return UpdateExistingResultComponent().run(result)

        return UpsertResultComponent().run(result)
