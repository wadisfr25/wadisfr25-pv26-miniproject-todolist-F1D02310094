import sqlite3
from pathlib import Path

from models.student import StudentProfile
from models.todo import TodoItem


class DatabaseManager:
    def __init__(self) -> None:
        self.db_path = Path(__file__).resolve().parent / "todo_list.db"
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    notes TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS student_profile (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    name TEXT NOT NULL,
                    nim TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def create_todo(self, item: TodoItem) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO todos (title, category, priority, due_date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item.title,
                    item.category,
                    item.priority,
                    item.due_date,
                    item.status,
                    item.notes,
                ),
            )
            connection.commit()

    def update_todo(self, item: TodoItem) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE todos
                SET title = ?, category = ?, priority = ?, due_date = ?, status = ?, notes = ?
                WHERE id = ?
                """,
                (
                    item.title,
                    item.category,
                    item.priority,
                    item.due_date,
                    item.status,
                    item.notes,
                    item.id,
                ),
            )
            connection.commit()

    def delete_todo(self, item_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM todos WHERE id = ?", (item_id,))
            connection.commit()

    def fetch_all_todos(self) -> list[TodoItem]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, title, category, priority, due_date, status, notes
                FROM todos
                ORDER BY due_date ASC, id DESC
                """
            ).fetchall()

        return [
            TodoItem(
                id=row[0],
                title=row[1],
                category=row[2],
                priority=row[3],
                due_date=row[4],
                status=row[5],
                notes=row[6],
            )
            for row in rows
        ]

    def fetch_todo_by_id(self, item_id: int) -> TodoItem | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, title, category, priority, due_date, status, notes
                FROM todos
                WHERE id = ?
                """,
                (item_id,),
            ).fetchone()

        if row is None:
            return None

        return TodoItem(
            id=row[0],
            title=row[1],
            category=row[2],
            priority=row[3],
            due_date=row[4],
            status=row[5],
            notes=row[6],
        )

    def save_student_profile(self, profile: StudentProfile) -> None:
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT id FROM student_profile WHERE id = 1"
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO student_profile (id, name, nim)
                    VALUES (1, ?, ?)
                    """,
                    (profile.name, profile.nim),
                )
            else:
                connection.execute(
                    """
                    UPDATE student_profile
                    SET name = ?, nim = ?
                    WHERE id = 1
                    """,
                    (profile.name, profile.nim),
                )
            connection.commit()

    def fetch_student_profile(self) -> StudentProfile | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, nim FROM student_profile WHERE id = 1"
            ).fetchone()

        if row is None:
            return None

        return StudentProfile(id=row[0], name=row[1], nim=row[2])
    