from datetime import date

import pytest

from models import Project, Task, User
from tasks import (
    assign_task,
    create_task,
    filter_tasks_by_status,
    get_status,
    iter_upcoming_tasks,
    sort_tasks_by_urgency,
    task_statistics,
    update_progress,
)


def make_tasks():
    project = Project(1, "Task Planner")
    tasks = []
    create_task(tasks, project, "Новая задача", date(2026, 10, 2), 2)
    create_task(tasks, project, "Срочная задача", date(2026, 9, 25), 5)
    return tasks


def test_task_object_and_project_connection():
    project = Project(1, "Task Planner")
    task = Task(1, project, "Написать тесты", date(2026, 10, 2))
    assert task.project is project
    assert task.status == "Новая"
    assert "Написать тесты" in str(task)


def test_user_validation_and_string():
    user = User("Иванов И.И.", "developer")
    assert user.role == "developer"
    assert str(user) == "Иванов И.И. (developer)"


def test_status_boundaries():
    assert get_status(0) == "Новая"
    assert get_status(50) == "В работе"
    assert get_status(100) == "Завершена"


def test_assign_and_update_progress():
    tasks = make_tasks()
    assign_task(tasks, 1, "Иванов И.И.", "developer")
    update_progress(tasks, 1, 40)
    assert tasks[0].assignee.name == "Иванов И.И."
    assert tasks[0].progress == 40


def test_invalid_role_is_rejected():
    tasks = make_tasks()
    with pytest.raises(ValueError, match="Роль"):
        assign_task(tasks, 1, "Петров П.П.", "manager")


def test_filter_and_statistics():
    tasks = make_tasks()
    update_progress(tasks, 2, 100)
    assert filter_tasks_by_status(tasks, "Завершена") == [tasks[1]]
    assert task_statistics(tasks) == {
        "total": 2,
        "new": 1,
        "in_progress": 0,
        "completed": 1,
        "average_progress": 50.0,
    }


def test_sort_and_upcoming_generator():
    tasks = make_tasks()
    today = date(2026, 9, 24)
    sorted_tasks = sort_tasks_by_urgency(tasks, today)
    assert sorted_tasks[0].title == "Срочная задача"
    upcoming = list(iter_upcoming_tasks(tasks, today, days=3))
    assert upcoming == [tasks[1]]
