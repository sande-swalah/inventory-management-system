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
        summary = self.get_summary()
        report = {
            "name": name,
            "summary": str(summary),
            "generated_on": datetime.now().isoformat(),
            "generated_for_user_id": generated_for_user_id,
        }
        return self.report_repo.create_report(report)

    def update_report(self, report_id, data):
        return self.report_repo.update_report(report_id, data)

    def remove_report(self, report_id):
        return self.report_repo.delete_report(report_id)
