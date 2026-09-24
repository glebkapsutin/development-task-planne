import pytest

from projects import add_project, find_projects, get_project


def test_add_and_find_project():
    projects = []
    created = add_project(projects, "Task Planner", "Учебный проект")
    assert created["id"] == 1
    assert find_projects(projects, "planner") == [created]


def test_get_unknown_project_raises_error():
    with pytest.raises(ValueError, match="не найден"):
        get_project([], 99)
