from abc import ABC

from simple_console import AbstractComponent
from simple_console import InputField
from simple_console import display_message
from simple_console import RunItem, RUN_END

from lab01.components.shared.validators import validate_filename
from lab01.components.shared.app_context import AppContext
from lab01.core.result import Result
from lab01.utility.parsers import parse_optional


class UpsertResultComponent(AbstractComponent[AppContext], ABC):
    filename_field: InputField[str | None]

    def declare_fields(self) -> None:
        if self.context.result_storage.file_count > 0:
            prompt = (
                "Ім’я існуючого файлу або нового файлу (до 5 літер українського й латинського алфавіту і/або цифр) "
                "чи символ * у разі відмови від запису й завершення програми: "
            )
        else:
            prompt = (
                "Ім’я нового файлу (до 5 літер українського й латинського алфавіту і/або цифр) "
                "чи символ * у разі відмови від запису й завершення програми: "
            )

        self.filename_field = InputField(
            prompt=prompt,
            parser=parse_optional(null="*"),
            validator=validate_filename
        )

    def run(self, result: Result) -> RunItem:
        filename = self.filename_field.get_input()

        if filename is None:
            display_message("Дані у файл не записано")
            return RUN_END

        result_storage = self.context.result_storage
        result_storage.write_result(filename, result)
        return RUN_END
