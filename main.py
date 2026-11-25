from storage_handler import StorageHandler
from student_manager import StudentManager
from attendance_manager import AttendanceManager
from report_generator import ReportGenerator
from visualizer import Visualizer

MENU = """
===== Student Attendance Management System =====
1. Add student          5. Mark attendance (one student)
2. Update student       6. Mark whole class (enter absentees)
3. Delete student       7. Reports (summary / defaulters / CSV)
4. List students        8. Charts
0. Exit
"""


def main():
    storage = StorageHandler()
    students = StudentManager(storage)
    attendance = AttendanceManager(storage, students)
    report = ReportGenerator(storage)
    viz = Visualizer(report)

    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                ok = students.add_student(
                    input("Roll no: "), input("Name: "),
                    input("Course: "), input("Semester: "))
                print("Added." if ok else "Roll no already exists.")
            elif choice == "2":
                ok = students.update_student(
                    input("Roll no: "),
                    input("New name (blank=keep): ") or None,
                    input("New course (blank=keep): ") or None,
                    input("New semester (blank=keep): ") or None)
                print("Updated." if ok else "Student not found.")
            elif choice == "3":
                print("Deleted." if students.delete_student(input("Roll no: "))
                      else "Student not found.")
            elif choice == "4":
                for row in students.list_students():
                    print(row)
            elif choice == "5":
                ok = attendance.mark(
                    input("Roll no: "), input("Subject: "),
                    input("P/A: "), input("Date YYYY-MM-DD (blank=today): ") or None)
                print("Marked." if ok else "Student not found.")
            elif choice == "6":
                absentees = input("Absent roll nos (comma separated, blank=none): ")
                n = attendance.mark_class(
                    input("Subject: "),
                    [r for r in absentees.split(",") if r.strip()],
                    input("Date YYYY-MM-DD (blank=today): ") or None)
                print(f"Marked {n} students.")
            elif choice == "7":
                print(report.student_summary().to_string(index=False))
                print("\nDefaulters:")
                print(report.defaulters().to_string(index=False))
                print("Saved:", report.export_csv())
            elif choice == "8":
                for fn in (viz.student_percent_chart, viz.monthly_trend_chart,
                           viz.subject_chart):
                    print("Saved:", fn())
            elif choice == "0":
                storage.close()
                break
            else:
                print("Invalid choice.")
        except ValueError as e:
            print("Input error:", e)


if __name__ == "__main__":
    main()
