# TaskFlow

TaskFlow adalah aplikasi desktop manajemen tugas harian yang dibuat dengan Python, PySide6, dan SQLite. Aplikasi ini membantu pengguna mencatat, mengedit, menghapus, dan memantau daftar tugas beserta kategori, prioritas, deadline, status, dan catatan tambahan.

## Fitur Utama

- Menambahkan tugas baru
- Mengubah data tugas
- Menghapus tugas
- Menampilkan daftar tugas dalam tabel
- Mengatur profil mahasiswa berupa nama dan NIM
- Menyimpan data secara lokal menggunakan SQLite

## Cara Menjalankan

1. Clone repository ini lalu masuk ke folder project.

```bash
git clone <url-repository>
cd wadisfr25-pv26-miniproject-todolist-F1D02310094
```

2. Buat virtual environment.

```bash
python -m venv venv
```

3. Aktifkan virtual environment.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
venv\Scripts\activate.bat
```

4. Install dependency.

```bash
pip install -r requirements.txt
```

5. Jalankan aplikasi.

```bash
python main.py
```

## Teknologi yang Digunakan

- Python
- PySide6
- SQLite
- Qt Style Sheet (QSS)

## Struktur Singkat Project

- `main.py` sebagai entry point aplikasi
- `controller/` untuk logika kontrol aplikasi
- `views/` untuk tampilan antarmuka
- `models/` untuk representasi data
- `database/` untuk pengelolaan database SQLite
- `styles/` untuk stylesheet tampilan aplikasi
