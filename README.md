# Student Attendance Management System

CLI app: Python, OOP, SQLite3, Pandas, Matplotlib/Seaborn, logging.

## Run
    pip install pandas matplotlib seaborn
    python main.py

## Structure
- storage_handler.py   : SQLite connection + tables
- student_manager.py   : add/update/delete/list students
- attendance_manager.py: mark attendance (single / whole class)
- report_generator.py  : Pandas summaries, defaulters (<75%), CSV export
- visualizer.py        : student %, monthly trend, subject-wise charts
- logger_setup.py      : logging to attendance.log
