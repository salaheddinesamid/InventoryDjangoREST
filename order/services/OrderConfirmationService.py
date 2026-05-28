from django.db import transaction
from ..models import Order


class OrderConfirmationService:

    @staticmethod
    @transaction.atomic()
    def confirm_order(order_id):
        # Fetch the order from the database
        order = Order.objects.get(
            id=order_id
        )

        # Check if the order exists
        if order is None:
            raise Order.DoesNotExist()
        # update the order status
        order.status = "CONFIRMED"
        return order
