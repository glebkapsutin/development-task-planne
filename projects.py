"""Функции для работы с коллекцией проектов."""

from models import Project


def add_project(
    projects: list[Project], name: str, description: str = ""
) -> Project:
    """Создать проект и добавить его в коллекцию."""
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Название проекта не может быть пустым")
    project = Project(
        max((item.id for item in projects), default=0) + 1,
        clean_name,
        description.strip(),
    )
    projects.append(project)
    return project


def find_projects(projects: list[Project], query: str) -> list[Project]:
    """Найти проекты по части названия без учёта регистра."""
    normalized = query.strip().lower()
    return [
        project for project in projects if normalized in project.name.lower()
    ]


def get_project(projects: list[Project], project_id: int) -> Project:
    """Получить проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project
    raise ValueError(f"Проект с id={project_id} не найден")
