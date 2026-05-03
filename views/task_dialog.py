from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from models.todo import TodoItem


class TaskDialog(QDialog):
    def __init__(self, parent=None, todo_item: TodoItem | None = None) -> None:
        super().__init__(parent)
        self.todo_item = todo_item
        self.setWindowTitle("Form Tugas")
        self.setMinimumWidth(440)

        self.title_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Kuliah", "Pribadi", "Organisasi", "Lainnya"])

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Tinggi", "Sedang", "Rendah"])

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setDisplayFormat("dd-MM-yyyy")

        self.status_input = QComboBox()
        self.status_input.addItems(["Belum Mulai", "Dikerjakan", "Selesai"])

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Catatan tambahan tugas")

        form_layout = QFormLayout()
        form_layout.addRow("Judul Tugas", self.title_input)
        form_layout.addRow("Kategori", self.category_input)
        form_layout.addRow("Prioritas", self.priority_input)
        form_layout.addRow("Deadline", self.due_date_input)
        form_layout.addRow("Status", self.status_input)
        form_layout.addRow("Catatan", self.notes_input)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self._validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        if self.todo_item:
            self._populate_form()

    def _populate_form(self) -> None:
        self.title_input.setText(self.todo_item.title)
        self.category_input.setCurrentText(self.todo_item.category)
        self.priority_input.setCurrentText(self.todo_item.priority)
        self.due_date_input.setDate(
            QDate.fromString(self.todo_item.due_date, "dd-MM-yyyy")
        )
        self.status_input.setCurrentText(self.todo_item.status)
        self.notes_input.setPlainText(self.todo_item.notes)

    def _validate_and_accept(self) -> None:
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Validasi", "Judul tugas wajib diisi.")
            return
        if not self.notes_input.toPlainText().strip():
            QMessageBox.warning(self, "Validasi", "Catatan tugas wajib diisi.")
            return
        self.accept()

    def get_todo_data(self) -> TodoItem:
        return TodoItem(
            id=self.todo_item.id if self.todo_item else None,
            title=self.title_input.text().strip(),
            category=self.category_input.currentText(),
            priority=self.priority_input.currentText(),
            due_date=self.due_date_input.date().toString("dd-MM-yyyy"),
            status=self.status_input.currentText(),
            notes=self.notes_input.toPlainText().strip(),
        )
