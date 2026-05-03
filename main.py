import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from controller.todo_controller import TodoController
from database.db_manager import DatabaseManager
from views.main_window import MainWindow


def load_stylesheet() -> str:
    style_path = Path(__file__).parent / "styles" / "app.qss"
    if style_path.exists():
        return style_path.read_text(encoding="utf-8")
    return ""


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    db_manager = DatabaseManager()
    window = MainWindow()
    window.controller = TodoController(window, db_manager)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
