"""Вспомогательные функции консольного интерфейса."""

from datetime import date, datetime


def parse_date(value: str) -> date:
    """Распознать дату в форматах ДД.ММ.ГГГГ и ГГГГ-ММ-ДД."""
    cleaned = value.strip()
    for pattern in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned, pattern).date()
        except ValueError:
            continue
    raise ValueError("Введите дату в формате ДД.ММ.ГГГГ")


def input_int(prompt: str, minimum: int, maximum: int) -> int:
    """Запросить целое число из заданного диапазона."""
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Введите число от {minimum} до {maximum}.")
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить корректную календарную дату."""
    while True:
        try:
            return parse_date(input(prompt))
        except ValueError as error:
            print(error)
