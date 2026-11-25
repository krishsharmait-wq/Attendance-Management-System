import pandas as pd
from logger_setup import get_logger


class ReportGenerator:
    def __init__(self, storage, threshold=75.0):
        self.storage = storage
        self.threshold = threshold
        self.log = get_logger()

    def load_data(self):
        query = """
            SELECT s.roll_no, s.name, a.subject, a.date, a.status
            FROM attendance a JOIN students s ON s.student_id = a.student_id
        """
        df = pd.read_sql_query(query, self.storage.conn)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df["present"] = (df["status"] == "P").astype(int)
        return df

    def student_summary(self):
        df = self.load_data()
        if df.empty:
            return df
        out = (df.groupby(["roll_no", "name"])
                 .agg(total=("present", "count"), attended=("present", "sum"))
                 .reset_index())
        out["percent"] = (out["attended"] / out["total"] * 100).round(2)
        return out.sort_values("percent")

    def subject_summary(self):
        df = self.load_data()
        if df.empty:
            return df
        out = (df.groupby("subject")["present"].mean() * 100).round(2)
        return out.reset_index(name="percent")

    def defaulters(self):
        summary = self.student_summary()
        if summary.empty:
            return summary
        return summary[summary["percent"] < self.threshold]

    def export_csv(self, path="attendance_report.csv"):
        summary = self.student_summary()
        summary.to_csv(path, index=False)
        self.log.info("Exported report to %s", path)
        return path
