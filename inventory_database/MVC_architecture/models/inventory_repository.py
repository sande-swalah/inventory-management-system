from flask import jsonify
from marshmallow import ValidationError

from extensions import db
from inventory_database.MVC_architecture.models.inventory_domain import Inventory_Data
from inventory_database.MVC_architecture.schemas.inventory_schema import InventorySchema


inventory_schema = InventorySchema()
list_inventory_schema = InventorySchema(many=True)

class InventoryRepository:

    def create_data(self, obj):
        try:
            new_data = inventory_schema.load(
                obj
            )
        except ValidationError as err:
            return jsonify({
                "err": err.messages
            }), 422
        
        db.session.add(new_data)
        db.session.commit()

        return inventory_schema.dump(new_data)
    
    def read_data(self, id):
        try:
            new_data = inventory_schema.load(
                {"id": id}
            )
        except ValidationError as err:
            return jsonify({
                "err": err.messages
            }), 422

        return inventory_schema.dump(new_data)
    
    def read_all_data(self):
        try:
            new_data = list_inventory_schema.load()

            return list_inventory_schema.dump(new_data)
        
        except ValidationError as err:
            return jsonify({
              "err": err.messages
                }), 422 
        
    def update_data(self, id, obj):
        try:
            new_data = inventory_schema.load(
                {"id": id}
            )
        except ValidationError as err:
            return jsonify({
                "err": err.messages
            }), 422

        if not new_data:
            return jsonify({
                "err": "Data not found"
            }), 404
        
        try:    
            updated_data = inventory_schema.load(
                obj
            )
        except ValidationError as err:
            return jsonify({
                "err": err.messages
            }), 422
        
        
        new_data.id = updated_data.id
        new_data.product_id = updated_data.product_id
        new_data.store_id = updated_data.store_id
        new_data.quantity = updated_data.quantity
        new_data.threshold = updated_data.threshold
        new_data.last_updated = updated_data.last_updated

    
   
        db.session.commit()
        
        return inventory_schema.dump(new_data)
    
    def delete_data(self, id):
        try:
            new_data = inventory_schema.load(
                {"id": id}
            )
        except ValidationError as err:
            return jsonify({
                "err": err.messages
            }), 422

        if not new_data:
            return jsonify({
                "err": "Data not found"
            }), 404

        db.session.delete(new_data)
        db.session.commit()

        return inventory_schema.dump(new_data)
