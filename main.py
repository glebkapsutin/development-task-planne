"""Консольное приложение для планирования задач разработки."""

from datetime import date
from pathlib import Path

from models import Project, Task
from projects import add_project, get_project
from storage import load_projects, load_tasks, save_records
from tasks import (
    assign_task,
    create_task,
    filter_tasks_by_status,
    find_tasks,
    get_status,
    get_urgency,
    iter_upcoming_tasks,
    sort_tasks_by_urgency,
    task_statistics,
    update_progress,
)
from utils import input_date, input_int

DATA_DIR = Path(__file__).parent / "data"
PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"


def show_projects(projects: list[Project]) -> None:
    """Вывести проекты."""
    if not projects:
        print("Проектов пока нет.")
        return
    for project in projects:
        print(f'{project["id"]}. {project["name"]} — {project["description"]}')


def show_tasks(tasks: list[Task], projects: list[Project]) -> None:
    """Вывести задачи и вычисляемые показатели."""
    if not tasks:
        print("Задач пока нет.")
        return
    for task in tasks:
        project = get_project(projects, task["project_id"])
        deadline = date.fromisoformat(task["deadline"])
        days_left = (deadline - date.today()).days
        assignee = task["assignee"] or "не назначен"
        print(
            f'#{task["id"]} [{get_status(task["progress"])}] '
            f'{task["title"]} | проект: {project["name"]} | '
            f'исполнитель: {assignee} | прогресс: {task["progress"]}% | '
            f'дедлайн: {deadline:%d.%m.%Y} | '
            f'срочность: {get_urgency(task["priority"], days_left)}'
        )


def print_menu() -> None:
    """Вывести главное меню."""
    print("\n=== Development Task Planner ===")
    print("1. Показать проекты")
    print("2. Добавить проект")
    print("3. Показать задачи")
    print("4. Добавить задачу")
    print("5. Найти задачу")
    print("6. Назначить исполнителя")
    print("7. Изменить прогресс")
    print("8. Фильтр по статусу")
    print("9. Сортировка по срочности")
    print("10. Ближайшие дедлайны")
    print("11. Статистика")
    print("0. Выход")


def main() -> None:
    """Запустить цикл консольного интерфейса."""
    try:
        projects = load_projects(PROJECTS_FILE)
        tasks = load_tasks(TASKS_FILE)
    except ValueError as error:
        print(f"Ошибка загрузки: {error}")
        return

    while True:
        print_menu()
        choice = input_int("Выберите действие: ", 0, 11)
        try:
            if choice == 0:
                print("Данные сохранены. До свидания!")
                break
            if choice == 1:
                show_projects(projects)
            elif choice == 2:
                project = add_project(
                    projects,
                    input("Название проекта: "),
                    input("Описание: "),
                )
                save_records(PROJECTS_FILE, projects)
                print(f'Проект «{project["name"]}» добавлен.')
            elif choice == 3:
                show_tasks(tasks, projects)
            elif choice == 4:
                show_projects(projects)
                project_id = input_int("ID проекта: ", 1, 1_000_000)
                get_project(projects, project_id)
                task = create_task(
                    tasks,
                    project_id,
                    input("Название задачи: "),
                    input_date("Дедлайн (ДД.ММ.ГГГГ): "),
                    input_int("Приоритет (1-5): ", 1, 5),
                    input("Описание: "),
                )
                save_records(TASKS_FILE, tasks)
                print(f'Задача «{task["title"]}» добавлена.')
            elif choice == 5:
                show_tasks(find_tasks(tasks, input("Поисковый запрос: ")), projects)
            elif choice == 6:
                task = assign_task(
                    tasks,
                    input_int("ID задачи: ", 1, 1_000_000),
                    input("Исполнитель: "),
                    input("Роль (developer/tester/teamlead): "),
                )
                save_records(TASKS_FILE, tasks)
                print(f'Исполнитель назначен на задачу «{task["title"]}».')
            elif choice == 7:
                task = update_progress(
                    tasks,
                    input_int("ID задачи: ", 1, 1_000_000),
                    input_int("Прогресс (0-100): ", 0, 100),
                )
                save_records(TASKS_FILE, tasks)
                print(f'Новый статус: {get_status(task["progress"])}.')
            elif choice == 8:
                status = input("Статус (Новая/В работе/Завершена): ")
                show_tasks(filter_tasks_by_status(tasks, status), projects)
            elif choice == 9:
                show_tasks(sort_tasks_by_urgency(tasks), projects)
            elif choice == 10:
                days = input_int("Период в днях: ", 1, 365)
                show_tasks(list(iter_upcoming_tasks(tasks, days=days)), projects)
            elif choice == 11:
                stats = task_statistics(tasks)
                print(
                    f'Всего: {stats["total"]}; новых: {stats["new"]}; '
                    f'в работе: {stats["in_progress"]}; '
                    f'завершено: {stats["completed"]}; '
                    f'средний прогресс: {stats["average_progress"]}%'
                )
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
