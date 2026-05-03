from PySide6.QtWidgets import QMessageBox

from database.db_manager import DatabaseManager
from models.student import StudentProfile
from models.todo import TodoItem
from views.main_window import MainWindow
from views.student_dialog import StudentDialog
from views.task_dialog import TaskDialog


class TodoController:
    def __init__(self, window: MainWindow, db_manager: DatabaseManager) -> None:
        self.window = window
        self.db_manager = db_manager
        self._connect_signals()
        self.load_student_profile()
        self.load_todos()

    def _connect_signals(self) -> None:
        self.window.add_button.clicked.connect(self.add_todo)
        self.window.edit_button.clicked.connect(self.edit_todo)
        self.window.delete_button.clicked.connect(self.delete_todo)
        self.window.refresh_button.clicked.connect(self.load_todos)
        self.window.profile_action.triggered.connect(self.manage_student_profile)
        self.window.about_action.triggered.connect(self.window.show_about_dialog)
        self.window.table.cellDoubleClicked.connect(self._handle_table_double_click)

    def load_student_profile(self) -> None:
        profile = self.db_manager.fetch_student_profile()
        if profile is None:
            self.window.set_student_profile(
                self.window.DEFAULT_STUDENT_NAME,
                self.window.DEFAULT_STUDENT_NIM,
            )
            return
        self.window.set_student_profile(profile.name, profile.nim)

    def manage_student_profile(self) -> None:
        current_profile = self.db_manager.fetch_student_profile()
        if current_profile is None:
            current_profile = StudentProfile(id=None, name="", nim="")

        dialog = StudentDialog(self.window, current_profile)
        if dialog.exec():
            self.db_manager.save_student_profile(dialog.get_profile_data())
            self.load_student_profile()
            QMessageBox.information(
                self.window,
                "Profil Tersimpan",
                "Data nama dan NIM berhasil diperbarui.",
            )

    def load_todos(self) -> None:
        items = self.db_manager.fetch_all_todos()
        self.window.populate_table(items)

    def add_todo(self) -> None:
        dialog = TaskDialog(self.window)
        if dialog.exec():
            self.db_manager.create_todo(dialog.get_todo_data())
            self.load_todos()

    def edit_todo(self) -> None:
        todo_item = self._get_selected_item()
        if not todo_item:
            QMessageBox.warning(
                self.window, "Peringatan", "Pilih satu tugas yang ingin diedit."
            )
            return

        dialog = TaskDialog(self.window, todo_item)
        if dialog.exec():
            self.db_manager.update_todo(dialog.get_todo_data())
            self.load_todos()

    def delete_todo(self) -> None:
        todo_item = self._get_selected_item()
        if not todo_item:
            QMessageBox.warning(
                self.window, "Peringatan", "Pilih satu tugas yang ingin dihapus."
            )
            return

        confirmation = QMessageBox.question(
            self.window,
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus tugas '{todo_item.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_todo(todo_item.id)
            self.load_todos()

    def _get_selected_item(self) -> TodoItem | None:
        todo_id = self.window.get_selected_todo_id()
        if todo_id is None:
            return None
        return self.db_manager.fetch_todo_by_id(todo_id)

    def _handle_table_double_click(self, _row: int, _column: int) -> None:
        if self.window.get_selected_todo_id() is not None:
            self.edit_todo()
