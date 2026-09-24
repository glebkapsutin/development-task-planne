"""Функции для работы с коллекцией задач."""

from collections.abc import Iterator
from datetime import date

from models import Project, Task, User


def get_status(progress: int) -> str:
    """Определить статус по проценту выполнения."""
    return Task.status_from_progress(progress)


def get_urgency(priority: int, days_left: int) -> int:
    """Рассчитать срочность по приоритету и числу оставшихся дней."""
    if not 1 <= priority <= 5:
        raise ValueError("Приоритет должен быть от 1 до 5")
    return int(priority * 10 / max(days_left + 1, 1))


def can_assign(role: str) -> bool:
    """Проверить, может ли роль использоваться для исполнителя."""
    return User.is_valid_role(role)


def create_task(
    tasks: list[Task],
    project: Project,
    title: str,
    deadline: date,
    priority: int = 3,
    description: str = "",
) -> Task:
    """Создать задачу и добавить её в коллекцию."""
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Название задачи не может быть пустым")
    if not 1 <= priority <= 5:
        raise ValueError("Приоритет должен быть от 1 до 5")
    task = Task(
        task_id=max((item.id for item in tasks), default=0) + 1,
        project=project,
        title=clean_title,
        deadline=deadline,
        priority=priority,
        description=description.strip(),
    )
    tasks.append(task)
    return task


def get_task(tasks: list[Task], task_id: int) -> Task:
    """Получить задачу по идентификатору."""
    for task in tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"Задача с id={task_id} не найдена")


def assign_task(
    tasks: list[Task], task_id: int, assignee: str, role: str
) -> Task:
    """Создать исполнителя и назначить его задаче."""
    task = get_task(tasks, task_id)
    task.assign(User(assignee, role))
    return task


def update_progress(tasks: list[Task], task_id: int, progress: int) -> Task:
    """Обновить прогресс задачи."""
    task = get_task(tasks, task_id)
    task.update_progress(progress)
    return task


def find_tasks(tasks: list[Task], query: str) -> list[Task]:
    """Найти задачи по названию или описанию."""
    normalized = query.strip().lower()
    return [
        task
        for task in tasks
        if normalized in task.title.lower()
        or normalized in task.description.lower()
    ]


def filter_tasks_by_status(tasks: list[Task], status: str) -> list[Task]:
    """Отфильтровать задачи по вычисляемому статусу."""
    normalized = status.strip().lower()
    return [task for task in tasks if task.status.lower() == normalized]


def sort_tasks_by_urgency(
    tasks: list[Task], today: date | None = None
) -> list[Task]:
    """Вернуть задачи от наиболее срочной к наименее срочной."""
    return sorted(tasks, key=lambda task: task.urgency(today), reverse=True)


def iter_upcoming_tasks(
    tasks: list[Task], today: date | None = None, days: int = 7
) -> Iterator[Task]:
    """Сгенерировать незавершённые задачи с ближайшим дедлайном."""
    current_date = today or date.today()
    for task in tasks:
        days_left = (task.deadline - current_date).days
        if 0 <= days_left <= days and task.progress < 100:
            yield task


def task_statistics(tasks: list[Task]) -> dict[str, int | float]:
    """Подсчитать задачи по статусам и средний прогресс."""
    counts = {"Новая": 0, "В работе": 0, "Завершена": 0}
    for task in tasks:
        counts[task.status] += 1
    average = sum(task.progress for task in tasks) / len(tasks) if tasks else 0.0
    return {
        "total": len(tasks),
        "new": counts["Новая"],
        "in_progress": counts["В работе"],
        "completed": counts["Завершена"],
        "average_progress": round(average, 1),
    }
