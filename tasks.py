"""Бизнес-логика системы планирования задач."""

from collections.abc import Iterator
from datetime import date

from models import Task

VALID_ROLES = {"developer", "tester", "teamlead"}


def get_status(progress: int) -> str:
    """Определить статус задачи по проценту выполнения."""
    if not 0 <= progress <= 100:
        raise ValueError("Прогресс должен быть от 0 до 100")
    if progress == 100:
        return "Завершена"
    if progress > 0:
        return "В работе"
    return "Новая"


def get_urgency(priority: int, days_left: int) -> int:
    """Рассчитать срочность: чем ближе дедлайн, тем выше значение."""
    if not 1 <= priority <= 5:
        raise ValueError("Приоритет должен быть от 1 до 5")
    return int(priority * 10 / max(days_left + 1, 1))


def can_assign(role: str) -> bool:
    """Проверить, может ли пользователь быть исполнителем задачи."""
    return role.strip().lower() in VALID_ROLES


def create_task(
    tasks: list[Task],
    project_id: int,
    title: str,
    deadline: date,
    priority: int = 3,
    description: str = "",
) -> Task:
    """Создать задачу с начальным прогрессом 0%."""
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Название задачи не может быть пустым")
    if not 1 <= priority <= 5:
        raise ValueError("Приоритет должен быть от 1 до 5")
    task = Task(
        id=max((item["id"] for item in tasks), default=0) + 1,
        project_id=project_id,
        title=clean_title,
        description=description.strip(),
        priority=priority,
        progress=0,
        assignee="",
        assignee_role="",
        deadline=deadline.isoformat(),
    )
    tasks.append(task)
    return task


def get_task(tasks: list[Task], task_id: int) -> Task:
    """Получить задачу по идентификатору."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Задача с id={task_id} не найдена")


def assign_task(
    tasks: list[Task], task_id: int, assignee: str, role: str
) -> Task:
    """Назначить задачу допустимому исполнителю."""
    clean_assignee = assignee.strip()
    clean_role = role.strip().lower()
    if not clean_assignee:
        raise ValueError("Имя исполнителя не может быть пустым")
    if not can_assign(clean_role):
        raise ValueError("Роль должна быть developer, tester или teamlead")
    task = get_task(tasks, task_id)
    task["assignee"] = clean_assignee
    task["assignee_role"] = clean_role
    return task


def update_progress(tasks: list[Task], task_id: int, progress: int) -> Task:
    """Обновить прогресс задачи."""
    get_status(progress)
    task = get_task(tasks, task_id)
    task["progress"] = progress
    return task


def find_tasks(tasks: list[Task], query: str) -> list[Task]:
    """Найти задачи по названию или описанию."""
    normalized = query.strip().lower()
    return [
        task
        for task in tasks
        if normalized in task["title"].lower()
        or normalized in task["description"].lower()
    ]


def filter_tasks_by_status(tasks: list[Task], status: str) -> list[Task]:
    """Отфильтровать задачи по вычисляемому статусу."""
    normalized = status.strip().lower()
    return [
        task
        for task in tasks
        if get_status(task["progress"]).lower() == normalized
    ]


def sort_tasks_by_urgency(
    tasks: list[Task], today: date | None = None
) -> list[Task]:
    """Вернуть задачи от наиболее срочной к наименее срочной."""
    current_date = today or date.today()
    return sorted(
        tasks,
        key=lambda task: get_urgency(
            task["priority"],
            (date.fromisoformat(task["deadline"]) - current_date).days,
        ),
        reverse=True,
    )


def iter_upcoming_tasks(
    tasks: list[Task], today: date | None = None, days: int = 7
) -> Iterator[Task]:
    """Сгенерировать незавершённые задачи с дедлайном в заданный период."""
    current_date = today or date.today()
    for task in tasks:
        days_left = (date.fromisoformat(task["deadline"]) - current_date).days
        if 0 <= days_left <= days and task["progress"] < 100:
            yield task


def task_statistics(tasks: list[Task]) -> dict[str, int | float]:
    """Подсчитать задачи по статусам и средний прогресс."""
    counts = {"Новая": 0, "В работе": 0, "Завершена": 0}
    for task in tasks:
        counts[get_status(task["progress"])] += 1
    average = (
        sum(task["progress"] for task in tasks) / len(tasks) if tasks else 0.0
    )
    return {
        "total": len(tasks),
        "new": counts["Новая"],
        "in_progress": counts["В работе"],
        "completed": counts["Завершена"],
        "average_progress": round(average, 1),
    }
