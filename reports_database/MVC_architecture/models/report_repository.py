
from extensions import db
from sqlalchemy.exc import IntegrityError, StatementError
from reports_database.MVC_architecture.models.report_domain import Report_Data
from reports_database.MVC_architecture.models.report_schema import ReportSchema


class ReportRepository:
    def __init__(self):
        self.schema = ReportSchema()
        self.list_schema = ReportSchema(many=True)

    def save_report(self, report):
        return self.create_report(report)

    def create_report(self, report):
        record = Report_Data(**report)
        db.session.add(record)
        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid report data")
        return self.schema.dump(record)

    def fetch_all_reports(self):
        records = Report_Data.query.order_by(Report_Data.generated_on.desc()).all()
        return self.list_schema.dump(records)

    def fetch_report(self, report_id):
        record = db.session.get(Report_Data, int(report_id))
        return self.schema.dump(record) if record else None

    def update_report(self, report_id, data):
        record = db.session.get(Report_Data, int(report_id))
        if not record:
            return None

        for field, value in data.items():
            setattr(record, field, value)

        try:
            db.session.commit()
        except (IntegrityError, StatementError):
            db.session.rollback()
            raise ValueError("Invalid report data")
        return self.schema.dump(record)

    def delete_report(self, report_id):
        record = db.session.get(Report_Data, int(report_id))
        if not record:
            return False

        db.session.delete(record)
        db.session.commit()
        return True
