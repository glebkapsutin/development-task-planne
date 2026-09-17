from datetime import date


task_name = "Реализовать API для списка задач"
priority = 4
progress = 30
assignee = "Иванов И.И."
deadline = date(2026, 9, 25)
today = date(2026, 9, 17)


# Функция 1. Статус задачи
def get_status(progress):
    if progress == 100:
        return "Завершена"
    elif progress > 0:
        return "В работе"
    else:
        return "Новая"


# Функция 2. Срочность задачи
def get_urgency(priority, days_left):
    score = priority * 10.0 / (days_left + 1)
    return int(score)


# Функция 3. Проверка назначения
def can_assign(role):
    if role == "developer":
        return True
    else:
        return False



days_left = (deadline - today).days
status = get_status(progress)
urgency = get_urgency(priority, days_left)
allowed = can_assign("developer")

print(f"Задача: {task_name}")
print(f"Исполнитель: {assignee}")
print(f"Дедлайн: {deadline}, осталось дней: {days_left}")
print(f"Статус: {status}")
print(f"Срочность: {urgency}")
print(f"Можно назначить: {str(allowed)}")