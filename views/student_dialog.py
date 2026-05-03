from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from models.student import StudentProfile


class StudentDialog(QDialog):
    def __init__(
        self, parent=None, profile: StudentProfile | None = None
    ) -> None:
        super().__init__(parent)
        self.profile = profile
        self.setWindowTitle("Profil Mahasiswa")
        self.setMinimumWidth(360)

        self.name_input = QLineEdit()
        self.nim_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Nama Mahasiswa", self.name_input)
        form_layout.addRow("NIM", self.nim_input)

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

        if self.profile:
            self.name_input.setText(self.profile.name)
            self.nim_input.setText(self.profile.nim)

    def _validate_and_accept(self) -> None:
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validasi", "Nama mahasiswa wajib diisi.")
            return
        if not self.nim_input.text().strip():
            QMessageBox.warning(self, "Validasi", "NIM wajib diisi.")
            return
        self.accept()

    def get_profile_data(self) -> StudentProfile:
        return StudentProfile(
            id=self.profile.id if self.profile else None,
            name=self.name_input.text().strip(),
            nim=self.nim_input.text().strip(),
        )
