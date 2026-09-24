"""Модель проекта разработки."""


class Project:
    """Проект разработки, объединяющий связанные задачи."""

    def __init__(self, project_id: int, name: str, description: str = ""):
        self.id = project_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"{self.name} - {self.description}" if self.description else self.name

    def to_dict(self) -> dict:
        """Подготовить данные проекта для сохранения в JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @classmethod
    def from_data(cls, data: dict) -> "Project":
        """Создать проект из данных JSON."""
        return cls(data["id"], data["name"], data.get("description", ""))
