"""Модель задачи разработки."""

from datetime import date
from typing import Optional

from .project import Project
from .user import User


class Task:
    """Задача, связанная с проектом и исполнителем."""

    def __init__(
        self,
        task_id: int,
        project: Project,
        title: str,
        deadline: date,
        priority: int = 3,
        description: str = "",
        progress: int = 0,
        assignee: Optional[User] = None,
    ):
        if not 1 <= priority <= 5:
            raise ValueError("Приоритет должен быть от 1 до 5")
        self.id = task_id
        self.project = project
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.assignee = assignee
        self.progress = 0
        self.update_progress(progress)

    @property
    def status(self) -> str:
        """Вернуть статус по текущему прогрессу."""
        return self.status_from_progress(self.progress)

    @staticmethod
    def status_from_progress(progress: int) -> str:
        """Определить статус по значению прогресса."""
        if not 0 <= progress <= 100:
            raise ValueError("Прогресс должен быть от 0 до 100")
        if progress == 100:
            return "Завершена"
        if progress > 0:
            return "В работе"
        return "Новая"

    def assign(self, user: User) -> None:
        """Назначить исполнителя."""
        self.assignee = user

    def update_progress(self, progress: int) -> None:
        """Изменить прогресс задачи."""
        self.status_from_progress(progress)
        self.progress = progress

    def urgency(self, today: Optional[date] = None) -> int:
        """Рассчитать срочность задачи."""
        current_date = today or date.today()
        days_left = (self.deadline - current_date).days
        return int(self.priority * 10 / max(days_left + 1, 1))

    def __str__(self) -> str:
        assignee = self.assignee.name if self.assignee else "не назначен"
        return (
            f"#{self.id} [{self.status}] {self.title} | "
            f"проект: {self.project.name} | исполнитель: {assignee} | "
            f"прогресс: {self.progress}% | "
            f"дедлайн: {self.deadline:%d.%m.%Y}"
        )

    def to_dict(self) -> dict:
        """Подготовить данные задачи для сохранения в JSON."""
        return {
            "id": self.id,
            "project_id": self.project.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "progress": self.progress,
            "assignee": self.assignee.name if self.assignee else "",
            "assignee_role": self.assignee.role if self.assignee else "",
            "deadline": self.deadline.isoformat(),
        }

    @classmethod
    def from_data(cls, data: dict, projects: list[Project]) -> "Task":
        """Создать задачу из JSON и восстановить связь с проектом."""
        project = next(
            (item for item in projects if item.id == data["project_id"]),
            None,
        )
        if project is None:
            raise ValueError(
                f'Проект с id={data["project_id"]} для задачи не найден'
            )
        assignee = None
        if data.get("assignee"):
            assignee = User(data["assignee"], data["assignee_role"])
        return cls(
            task_id=data["id"],
            project=project,
            title=data["title"],
            deadline=date.fromisoformat(data["deadline"]),
            priority=data.get("priority", 3),
            description=data.get("description", ""),
            progress=data.get("progress", 0),
            assignee=assignee,
        )
