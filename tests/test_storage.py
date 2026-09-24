import json
from datetime import date

import pytest

from models import Project, Task, User
from storage import (
    load_projects,
    load_records,
    load_tasks,
    save_records,
)


def test_save_and_load_objects(tmp_path):
    projects_path = tmp_path / "data" / "projects.json"
    tasks_path = tmp_path / "data" / "tasks.json"
    project = Project(1, "Task Planner", "Учебный проект")
    task = Task(
        1,
        project,
        "Написать тесты",
        date(2026, 10, 2),
        assignee=User("Иванов И.И.", "tester"),
    )
    save_records(projects_path, [project])
    save_records(tasks_path, [task])

    loaded_projects = load_projects(projects_path)
    loaded_tasks = load_tasks(tasks_path, loaded_projects)
    assert loaded_projects[0].name == "Task Planner"
    assert loaded_tasks[0].project is loaded_projects[0]
    assert loaded_tasks[0].assignee.role == "tester"


def test_missing_file_returns_empty_list(tmp_path):
    assert load_records(tmp_path / "missing.json") == []


def test_invalid_json_raises_clear_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="Некорректный JSON"):
        load_records(path)


def test_non_list_json_is_rejected(tmp_path):
    path = tmp_path / "object.json"
    path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(ValueError, match="список"):
        load_records(path)


def test_unknown_project_in_task_is_rejected(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "project_id": 99,
                    "title": "Задача",
                    "deadline": "2026-10-02",
                }
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Проект с id=99"):
        load_tasks(path, [])
