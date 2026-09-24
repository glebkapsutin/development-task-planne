"""Модель исполнителя задачи."""


class User:
    """Исполнитель задачи."""

    VALID_ROLES = {"developer", "tester", "teamlead"}

    def __init__(self, name: str, role: str):
        clean_name = name.strip()
        clean_role = role.strip().lower()
        if not clean_name:
            raise ValueError("Имя исполнителя не может быть пустым")
        if not self.is_valid_role(clean_role):
            raise ValueError("Роль должна быть developer, tester или teamlead")
        self.name = clean_name
        self.role = clean_role

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

    @staticmethod
    def is_valid_role(role: str) -> bool:
        """Проверить допустимость роли."""
        return role.strip().lower() in User.VALID_ROLES
