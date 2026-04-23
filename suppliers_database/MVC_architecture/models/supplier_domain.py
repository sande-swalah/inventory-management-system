from datetime import datetime

from extensions import db


class Supplier_Data(db.Model):
        __tablename__ = "suppliers"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        product = db.Column(db.String(100))
        category = db.Column(db.String(100))
        contact_number = db.Column(db.String(20))
        email = db.Column(db.String(100), unique=True)
        supplier_type = db.Column(db.String(50))
        not_taking_return = db.Column(db.Boolean, nullable=False, default=False)
        taking_return = db.Column(db.Boolean, nullable=False, default=False)
        created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        user_email = db.Column(db.String(100), db.ForeignKey("users.email"), unique=True, nullable=True)

        products = db.relationship("Product_Data", back_populates="supplier", lazy=True)
        inventory_items = db.relationship("Inventory_Data", back_populates="supplier", lazy=True)
        user = db.relationship(
                "User_Data",
                back_populates="supplier_profile",
                primaryjoin="Supplier_Data.user_email == User_Data.email",
                foreign_keys=[user_email],
        )


