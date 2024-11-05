import datetime as dt
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Final, Any

from lab01.core.result import Result

PROJECT_DIR: Final[Path] = Path(__file__).parent.parent.parent
STORAGE_DIR: Final[Path] = PROJECT_DIR / "files"
STORAGE_INFO_FILE: Final[Path] = STORAGE_DIR / ".info.json"

TABLE_HEADERS: Final[list[str]] = [
    "Дата (ДД.ММ.РРРР)",
    "Аргумент x",
    "Точність e",
    "Значення функції",
    "Кількість членів ряду N"
]
COLUMN_WIDTH: Final[int] = 25
COLUMN_DELIMITER: Final[str] = "| "
ROW_DELIMITER: Final[str] = "_"


@dataclass
class StorageInfo:
    last_used_file: str | None = None


class ResultStorage:
    def __init__(self) -> None:
        self._init()
        self._files = {file for file in STORAGE_DIR.iterdir() if file != STORAGE_INFO_FILE}

    def _init(self) -> None:
        STORAGE_DIR.mkdir(exist_ok=True)

        if not STORAGE_INFO_FILE.exists():
            self._write_storage_info(StorageInfo())

    @property
    def files(self) -> set[str]:
        return {file.name for file in self._files}

    @property
    def file_count(self) -> int:
        return len(self._files)

    @property
    def last_used_file(self) -> str | None:
        info = self._read_storage_info()
        return info.last_used_file

    def write_result(self, filename: str, result: Result) -> None:
        if not (STORAGE_DIR / filename).exists():
            self._create_file(filename)

        with open(STORAGE_DIR / filename, "a") as f:
            result_row = self._format_result(result)
            f.write(result_row)

        self._files.add(STORAGE_DIR / filename)
        self._write_storage_info(StorageInfo(last_used_file=filename))

    def _create_file(self, filename: str) -> None:
        with open(STORAGE_DIR / filename, "w") as f:
            table_row = self._format_row(TABLE_HEADERS)
            f.write(table_row)

    def _format_row(self, values: list[str]) -> str:
        data = COLUMN_DELIMITER.join(value.ljust(COLUMN_WIDTH) for value in values) + "\n"
        border = COLUMN_DELIMITER.join(ROW_DELIMITER * COLUMN_WIDTH for _ in values) + "\n"
        return data + border

    def _format_result(self, result: Result) -> str:
        date = dt.date.today()
        values = [
            date.strftime("%d.%m.%Y"),
            str(result.argument),
            str(result.precision),
            str(result.value),
            str(result.n_terms)
        ]
        return self._format_row(values)

    def _write_storage_info(self, storage_info: StorageInfo) -> None:
        with open(STORAGE_INFO_FILE, "w") as f:
            json.dump(asdict(storage_info), f, indent=2)

    def _read_storage_info(self) -> StorageInfo:
        with open(STORAGE_INFO_FILE, "r") as f:
            return StorageInfo(**json.load(f))
