from ..models.report_repository import ReportRepository
from ..services.report_service import ReportService
from products_database.MVC_architecture.models.product_repository import ProductRepository
from orders_database.MVC_architecture.models.order_repository import OrderRepository
from inventory_database.MVC_architecture.models.inventory_repository import InventoryRepository


class ReportController:
    def __init__(self, service, report_repo):
        self.service = service
        self.report_repo = report_repo

    def get_summary(self):
        return self.service.get_summary()

    def get_history(self):
        return self.report_repo.fetch_all_reports()

    def snapshot(self, name):
        return self.service.create_report_snapshot(name)


report_repository = ReportRepository()
report_service = ReportService(
    report_repository,
    ProductRepository(),
    OrderRepository(),
    InventoryRepository(),
)
report_controller = ReportController(report_service, report_repository)
