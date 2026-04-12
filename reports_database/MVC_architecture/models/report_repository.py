from reports_database import get_db


class ReportRepository:
    def save_report(self, report):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO reports (name, summary, generated_on)
            VALUES (?, ?, ?)
            """,
            (report["name"], report["summary"], report["generated_on"]),
        )
        db.commit()
        return cursor.lastrowid

    def fetch_all_reports(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reports ORDER BY generated_on DESC")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row):
        return {
            "id": row["id"],
            "name": row["name"],
            "summary": row["summary"],
            "generated_on": row["generated_on"],
        }
