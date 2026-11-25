import matplotlib
matplotlib.use("Agg")  # saves files; no GUI window needed
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    def __init__(self, report):
        self.report = report

    def student_percent_chart(self, path="student_attendance.png"):
        data = self.report.student_summary()
        if data.empty:
            return None
        plt.figure(figsize=(9, 5))
        sns.barplot(data=data, x="roll_no", y="percent")
        plt.axhline(self.report.threshold, color="red", linestyle="--",
                    label=f"{self.report.threshold:.0f}% limit")
        plt.title("Attendance % per Student")
        plt.ylim(0, 100)
        plt.legend()
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path

    def monthly_trend_chart(self, path="monthly_trend.png"):
        df = self.report.load_data()
        if df.empty:
            return None
        monthly = (df.groupby(df["date"].dt.to_period("M"))["present"].mean() * 100)
        plt.figure(figsize=(8, 4))
        plt.plot(monthly.index.astype(str), monthly.values, marker="o")
        plt.title("Monthly Attendance Trend (%)")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path

    def subject_chart(self, path="subject_attendance.png"):
        data = self.report.subject_summary()
        if data.empty:
            return None
        plt.figure(figsize=(8, 4))
        sns.barplot(data=data, x="subject", y="percent")
        plt.title("Subject-wise Attendance %")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path
