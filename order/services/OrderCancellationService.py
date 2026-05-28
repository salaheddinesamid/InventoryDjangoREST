from django.db import transaction
from ..models import Order
from stock.services.StockUpdateService import StockUpdateService


class OrderCancellationService:

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id):
        """

        :param order_id:
        :return:
        """

        # Fetch the order from the database:
        order = Order.objects.get(id=order_id)

        # Get the order items:
        order_items = order.items.all()

        # Check if the order is already cancelled:
        if order.status == "CANCELED":
            raise ValueError("The order has already been canceled")

        # Iterate over order items:
        for item in order_items:
            product = item.product
            # restore the product quantity
            StockUpdateService.restore_quantity(
                product_id=product.id,
                quantity=item.quantity
            )

        # Set the order status to 'CANCELED'
        order.status = "CANCELED"
        order.save()


