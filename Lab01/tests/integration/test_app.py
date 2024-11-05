import io
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from lab01.components.main_component import MainComponent


@pytest.fixture(scope="module")
def storage_dir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("storage_dir")
    return temp_dir


@pytest.mark.dependency()
def test_persist_first_file(storage_dir: Path):
    sys.stdin = io.StringIO(
        "1.0\n"  # Задайте аргумент функції
        "0.001\n"  # Задайте точність обчислення
        "Так\n"  # Записати результат у файл
        "рез1\n"  # Ім'я нового файлу
    )

    with patch("lab01.infrastructure.result_storage.STORAGE_DIR", storage_dir):
        MainComponent().run()

    result_file = storage_dir / "рез1"
    assert result_file.exists()
    assert result_file.stat().st_size > 0


@pytest.mark.dependency(depends=[test_persist_first_file.__name__])
def test_update_last_file(storage_dir: Path):
    last_file = storage_dir / "рез1"
    initial_size = last_file.stat().st_size

    sys.stdin = io.StringIO(
        "1.0\n"  # Задайте аргумент функції
        "0.001\n"  # Задайте точність обчислення
        "Так\n"  # Записати результат у файл
        "Так\n"  # Записати у файл 'рез1'
    )

    with patch("lab01.infrastructure.result_storage.STORAGE_DIR", storage_dir):
        MainComponent().run()

    assert last_file.stat().st_size > initial_size


@pytest.mark.dependency(depends=[test_persist_first_file.__name__])
def test_persist_new_file(storage_dir: Path):
    sys.stdin = io.StringIO(
        "1.0\n"  # Задайте аргумент функції
        "0.001\n"  # Задайте точність обчислення
        "Так\n"  # Записати результат у файл
        "Ні\n"  # Записати у файл 'рез1'
        "рез2"  # Ім'я нового файлу
    )

    with patch("lab01.infrastructure.result_storage.STORAGE_DIR", storage_dir):
        MainComponent().run()

    result_file = storage_dir / "рез2"
    assert result_file.exists()
    assert result_file.stat().st_size > 0
