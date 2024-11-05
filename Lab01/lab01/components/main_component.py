import math

from simple_console import AbstractComponent
from simple_console import InputField
from simple_console import display_message
from simple_console import RunItem

from lab01.components.shared.app_context import AppContext
from lab01.components.persist_result_component import PersistResultComponent
from lab01.core.function import f
from lab01.utility.validators import pipeline, greater_than, less_than


class MainComponent(AbstractComponent[AppContext]):
    argument_field: InputField[float]
    precision_field: InputField[float]

    def declare_fields(self) -> None:
        argument_min, argument_max = -math.pi / 2, math.pi / 2
        self.argument_field = InputField(
            prompt=f"Задайте аргумент функції (від {argument_min:.2f} до {argument_max:.2f}):",
            parser=float,
            validator=pipeline(greater_than(argument_min), less_than(argument_max))
        )
        self.precision_field = InputField(
            prompt="Задайте точність обчислення (від 0 до 1):",
            parser=float,
            validator=pipeline(greater_than(0.), less_than(1.))
        )

    def run(self) -> RunItem:
        argument = self.argument_field.get_input()
        precision = self.precision_field.get_input()

        result = f(argument, precision)
        display_message("Кінець")

        display_message(f"Значення функції: {result.value}")
        display_message(f"Кількість членів ряду N: {result.n_terms}")

        return PersistResultComponent().run(result)
