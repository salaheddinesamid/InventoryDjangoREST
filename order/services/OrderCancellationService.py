from django.db import transaction
from ..models import Order
from stock.services.StockUpdateService import StockUpdateService
import logging

logger = logging.getLogger("app_logger")


class OrderCancellationService:

    @staticmethod
    @transaction.atomic()
    def cancel_order(order_id):

        # 🔒 Lock order row to prevent concurrent cancellation
        order = Order.objects.select_for_update().get(id=order_id)

        if order.status == "CANCELED":
            raise ValueError("Order already canceled")

        order_items = order.items.select_related("product").all()

        for item in order_items:
            StockUpdateService.restore_quantity(
                product_id=item.product.id,
                quantity=item.quantity
            )

        order.status = "CANCELED"
        order.save()

        return order
