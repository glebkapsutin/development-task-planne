"""Загрузка и сохранение объектов Task Planner в JSON."""

import json
from pathlib import Path

from models import Project, Task


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


def save_records(path: Path, records: list[Project | Task | dict]) -> None:
    """Преобразовать объекты в словари и сохранить их в JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [item if isinstance(item, dict) else item.to_dict() for item in records]
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise ValueError(f"Не удалось сохранить данные в {path}") from error


def load_projects(path: Path) -> list[Project]:
    """Загрузить проекты как объекты Project."""
    return [Project.from_data(record) for record in load_records(path)]


def load_tasks(path: Path, projects: list[Project]) -> list[Task]:
    """Загрузить задачи и восстановить связи с проектами."""
    return [Task.from_data(record, projects) for record in load_records(path)]
