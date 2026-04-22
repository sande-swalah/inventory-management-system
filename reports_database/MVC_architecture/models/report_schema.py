from extensions import ma
from reports_database.MVC_architecture.models.report_domain import Report_Data


class ReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Report_Data
        include_fk = True
        load_instance = True
