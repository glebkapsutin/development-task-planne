"""Типы данных проекта Task Planner."""

from typing import TypedDict


class Project(TypedDict):
    """Проект разработки."""

    id: int
    name: str
    description: str


class Task(TypedDict):
    """Задача разработки, сохраняемая в JSON."""

    id: int
    project_id: int
    title: str
    description: str
    priority: int
    progress: int
    assignee: str
    assignee_role: str
    deadline: str
