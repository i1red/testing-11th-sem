from simple_console import display_message
from simple_console import RunItem, RUN_END
from simple_console import AbstractComponent
from simple_console import InputField

from lab01.components.shared.app_context import AppContext
from lab01.core.result import Result
from lab01.utility.parsers import parse_optional


class UpdateExistingResultComponent(AbstractComponent[AppContext]):
    filename_field: InputField[str | None]

    def declare_fields(self) -> None:
        self.filename_field = InputField(
            prompt="Ім’я існуючого файлу чи символ * у разі відмови від запису та завершення програми:",
            parser=parse_optional(null="*")
        )

    def run(self, result: Result) -> RunItem:
        filename = self.filename_field.get_input()

        if filename is None:
            display_message("Дані у файл не записано")
            return RUN_END

        result_storage = self.context.result_storage
        if filename not in result_storage.files:
            display_message("Файлу з вказаним ім'ям не існує")
            return self.run(result)

        result_storage.write_result(filename, result)
        return RUN_END
