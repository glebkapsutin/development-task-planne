"""Загрузка и сохранение данных Task Planner в JSON."""

import json
from pathlib import Path
from typing import TypeVar

from models import Project, Task

JsonRecord = TypeVar("JsonRecord", Project, Task)


def load_records(path: Path) -> list[dict]:
    """Загрузить список записей; отсутствующий файл считать пустым."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {path}") from error
    if not isinstance(data, list):
        raise ValueError(f"В файле {path} должен находиться список")
    return data


def save_records(path: Path, records: list[JsonRecord]) -> None:
    """Сохранить список записей, автоматически создав каталог."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise ValueError(f"Не удалось сохранить данные в {path}") from error


def load_projects(path: Path) -> list[Project]:
    """Загрузить проекты."""
    return [Project(**record) for record in load_records(path)]


def load_tasks(path: Path) -> list[Task]:
    """Загрузить задачи."""
    return [Task(**record) for record in load_records(path)]
