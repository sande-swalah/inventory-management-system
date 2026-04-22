from datetime import datetime

from extensions import db


class Report_Data(db.Model):
	__tablename__ = "reports"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	summary = db.Column(db.Text, nullable=False)
	generated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
