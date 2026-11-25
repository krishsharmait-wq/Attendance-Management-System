from datetime import date as dt
from logger_setup import get_logger


class AttendanceManager:
    def __init__(self, storage, student_manager):
        self.storage = storage
        self.students = student_manager
        self.log = get_logger()

    def mark(self, roll_no, subject, status, on_date=None):
        """status: 'P' or 'A'. Re-marking same day/subject overwrites."""
        status = status.upper()
        if status not in ("P", "A"):
            raise ValueError("status must be 'P' or 'A'")
        student = self.students.get_by_roll(roll_no)
        if not student:
            self.log.warning("Mark failed, unknown roll_no %s", roll_no)
            return False
        on_date = on_date or dt.today().isoformat()
        self.storage.execute(
            """INSERT INTO attendance (student_id, subject, date, status)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(student_id, subject, date)
               DO UPDATE SET status = excluded.status""",
            (student[0], subject.strip().title(), on_date, status),
        )
        self.log.info("Marked %s %s for %s on %s", roll_no, status, subject, on_date)
        return True

    def mark_class(self, subject, absent_rolls, on_date=None):
        """Everyone present except the roll numbers in absent_rolls."""
        absent = {r.strip() for r in absent_rolls}
        count = 0
        for roll_no, *_ in self.students.list_students():
            status = "A" if roll_no in absent else "P"
            if self.mark(roll_no, subject, status, on_date):
                count += 1
        return count
