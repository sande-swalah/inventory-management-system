from datetime import datetime

from extensions import db, ma


class Supplier_Data(db.Model):
        __tablename__ = "suppliers"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        product = db.Column(db.String(100))
        category = db.Column(db.String(100))
        contact_number = db.Column(db.String(20))
        email = db.Column(db.String(100), unique=True)
        supplier_type = db.Column(db.String(50))
        created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        products = db.relationship("Product_Data", back_populates="supplier", lazy=True)


