from datetime import datetime

from ..models.report_repository import ReportRepository
from products_database.MVC_architecture.models.product_repository import ProductRepository
from orders_database.MVC_architecture.models.order_repository import OrderRepository
from inventory_database.MVC_architecture.models.inventory_repository import InventoryRepository


class ReportService:
    def __init__(self, report_repo, product_repo, order_repo, inventory_repo):
        self.report_repo = report_repo
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.inventory_repo = inventory_repo

    def get_all_reports(self):
        return self.report_repo.fetch_all_reports()

    def get_report(self, report_id):
        return self.report_repo.fetch_report(report_id)

    def get_summary(self):
        products = self.product_repo.fetch_all_products()
        orders = self.order_repo.fetch_all_orders()
        inventory = self.inventory_repo.fetch_all_items()

        summary = {
            "total_products": len(products),
            "total_orders": len(orders),
            "total_inventory_items": len(inventory),
            "low_stock_items": [item for item in inventory if item["quantity"] <= item["threshold"]],
        }
        return summary

    def create_report_snapshot(self, name, generated_for_user_id=None):
        if not name:
            raise ValueError("Report name is required")

        summary = self.get_summary()
        report = {
            "name": name,
            "summary": str(summary),
            "generated_on": datetime.utcnow(),
            "generated_for_user_id": generated_for_user_id,
        }
        return self.report_repo.create_report(report)

    def update_report(self, report_id, data):
        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "name",
            "summary",
            "generated_on",
            "generated_for_user_id",
        }

        payload = {}
        for field, value in data.items():
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

            if field == "name" and (value is None or str(value).strip() == ""):
                raise ValueError("Report name cannot be empty")

            if field == "generated_on" and isinstance(value, str):
                normalized_value = value.replace("Z", "+00:00")
                try:
                    value = datetime.fromisoformat(normalized_value)
                except ValueError as exc:
                    raise ValueError("Invalid generated_on format. Use ISO datetime string") from exc

            payload[field] = value

        return self.report_repo.update_report(report_id, payload)

    def remove_report(self, report_id):
        return self.report_repo.delete_report(report_id)
