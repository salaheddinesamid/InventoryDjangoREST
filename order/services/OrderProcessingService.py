from django.db import transaction
from ..models import Order, OrderItem
from stock.models import Product
from stock.services.StockUpdateService import StockUpdateService


class OrderProcessingService:
    @staticmethod
    @transaction.atomic()
    def process_order(validated_data):
        # Create new order
        order = Order.objects.create()
        # Initiate order items
        order_items = []
        # Extract order items from the request
        items = validated_data['items']
        total_price = 0

        for item in items:
            try:
                order_item = OrderItem.objects.create(
                    quantity=0
                )
                product = Product.objects.get(id=item['product_id'])
                # Update the product quantity
                StockUpdateService.decrease_quantity(product.id, item['quantity'])

                item_price = product.price * item['quantity']

                order_item.product_id = product.id
                order_item.price = item_price

                # Increase the order total price
                total_price += item_price
            except Product.DoesNotExist:
                raise ValueError()

        order.total_amount = total_price
        order.status = "CREATED"
        order.save()
        return order
