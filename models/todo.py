from dataclasses import dataclass


@dataclass
class TodoItem:
    id: int | None
    title: str
    category: str
    priority: str
    due_date: str
    status: str
    notes: str
