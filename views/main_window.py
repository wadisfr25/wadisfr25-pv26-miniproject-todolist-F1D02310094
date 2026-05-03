from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.todo import TodoItem


class MainWindow(QMainWindow):
    APP_NAME = "TaskFlow"
    APP_DESCRIPTION = "Aplikasi manajemen tugas harian berbasis PySide6 dan SQLite."
    DEFAULT_STUDENT_NAME = "Belum diatur"
    DEFAULT_STUDENT_NIM = "Belum diatur"

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.APP_NAME)
        self.resize(980, 620)
        self._build_ui()
        self._build_menu()

    def _build_ui(self) -> None:
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        title_label = QLabel(self.APP_NAME)
        title_label.setObjectName("pageTitle")

        description_label = QLabel(self.APP_DESCRIPTION)
        description_label.setWordWrap(True)
        description_label.setObjectName("pageDescription")

        self.student_name_label = QLabel()
        self.student_nim_label = QLabel()
        self.student_name_label.setObjectName("identityLabel")
        self.student_nim_label.setObjectName("identityLabel")
        self.set_student_profile(
            self.DEFAULT_STUDENT_NAME,
            self.DEFAULT_STUDENT_NIM,
        )

        header_layout = QVBoxLayout()
        header_layout.addWidget(title_label)
        header_layout.addWidget(description_label)
        header_layout.addWidget(self.student_name_label)
        header_layout.addWidget(self.student_nim_label)

        self.add_button = QPushButton("Tambah Tugas")
        self.edit_button = QPushButton("Edit Tugas")
        self.delete_button = QPushButton("Hapus Tugas")
        self.refresh_button = QPushButton("Muat Ulang")

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.add_button)
        action_layout.addWidget(self.edit_button)
        action_layout.addWidget(self.delete_button)
        action_layout.addStretch()
        action_layout.addWidget(self.refresh_button)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Judul", "Kategori", "Prioritas", "Deadline", "Status", "Catatan"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setMinimumSectionSize(120)
        self.table.setColumnHidden(0, True)
        self.table.setAlternatingRowColors(True)

        self.status_label = QLabel("Total tugas: 0")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.status_label.setObjectName("footerLabel")

        main_layout.addLayout(header_layout)
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.status_label)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _build_menu(self) -> None:
        menu_bar = self.menuBar()
        profile_menu = menu_bar.addMenu("Profil")
        self.profile_action = QAction("Atur Nama dan NIM", self)
        profile_menu.addAction(self.profile_action)

        about_menu = menu_bar.addMenu("Tentang Aplikasi")
        self.about_action = QAction("Informasi Aplikasi", self)
        about_menu.addAction(self.about_action)

    def show_about_dialog(self) -> None:
        student_name = self.student_name_label.text().replace("Nama: ", "", 1)
        student_nim = self.student_nim_label.text().replace("NIM: ", "", 1)
        QMessageBox.information(
            self,
            "Tentang Aplikasi",
            (
                f"Nama Aplikasi: {self.APP_NAME}\n"
                f"Deskripsi: {self.APP_DESCRIPTION}\n"
                f"Nama Mahasiswa: {student_name}\n"
                f"NIM: {student_nim}"
            ),
        )

    def set_student_profile(self, name: str, nim: str) -> None:
        self.student_name_label.setText(f"Nama: {name}")
        self.student_nim_label.setText(f"NIM: {nim}")

    def populate_table(self, items: list[TodoItem]) -> None:
        self.table.setRowCount(0)
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            values = [
                str(item.id),
                item.title,
                item.category,
                item.priority,
                item.due_date,
                item.status,
                item.notes,
            ]
            for column, value in enumerate(values):
                table_item = QTableWidgetItem(value)
                table_item.setData(Qt.ItemDataRole.UserRole, item.id)
                if column == 3:
                    self._apply_priority_style(table_item, value)
                self.table.setItem(row, column, table_item)

        self.status_label.setText(f"Total tugas: {len(items)}")

    def get_selected_todo_id(self) -> int | None:
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return None
        row = selected_rows[0].row()
        id_item = self.table.item(row, 0)
        if id_item is None:
            return None
        try:
            return int(id_item.text())
        except ValueError:
            return None

    def _apply_priority_style(self, table_item: QTableWidgetItem, priority: str) -> None:
        if priority == "Tinggi":
            table_item.setBackground(QColor("#f8d7da"))
            table_item.setForeground(QColor("#842029"))
        elif priority == "Sedang":
            table_item.setBackground(QColor("#fff3cd"))
            table_item.setForeground(QColor("#664d03"))
        elif priority == "Rendah":
            table_item.setBackground(QColor("#d1e7dd"))
            table_item.setForeground(QColor("#0f5132"))
