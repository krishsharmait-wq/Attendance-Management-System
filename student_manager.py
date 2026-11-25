import sqlite3
from logger_setup import get_logger


class StudentManager:
    def __init__(self, storage):
        self.storage = storage
        self.log = get_logger()

    def add_student(self, roll_no, name, course, semester):
        try:
            self.storage.execute(
                "INSERT INTO students (roll_no, name, course, semester) VALUES (?, ?, ?, ?)",
                (roll_no.strip(), name.strip(), course.strip(), int(semester)),
            )
            self.log.info("Added student %s (%s)", name, roll_no)
            return True
        except sqlite3.IntegrityError:
            self.log.warning("Duplicate roll_no: %s", roll_no)
            return False

    def update_student(self, roll_no, name=None, course=None, semester=None):
        student = self.get_by_roll(roll_no)
        if not student:
            return False
        _, _, old_name, old_course, old_sem = student
        self.storage.execute(
            "UPDATE students SET name=?, course=?, semester=? WHERE roll_no=?",
            (name or old_name, course or old_course,
             int(semester) if semester else old_sem, roll_no),
        )
        self.log.info("Updated student %s", roll_no)
        return True

    def delete_student(self, roll_no):
        cur = self.storage.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
        deleted = cur.rowcount > 0
        if deleted:
            self.log.info("Deleted student %s", roll_no)
        return deleted

    def get_by_roll(self, roll_no):
        rows = self.storage.fetch_all(
            "SELECT * FROM students WHERE roll_no=?", (roll_no,)
        )
        return rows[0] if rows else None

    def list_students(self):
        return self.storage.fetch_all(
            "SELECT roll_no, name, course, semester FROM students ORDER BY roll_no"
        )
