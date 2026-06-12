from django.db import transaction
from ..models import Order, OrderItem
from stock.models import Product
from stock.services.StockUpdateService import StockUpdateService
from user_management.models import User


class OrderProcessingService:
    @staticmethod
    @transaction.atomic()
    def process_order(validated_data, user_email):

        try:
            # Fetch the user from the database:
            user = User.objects.get(
                email=user_email
            )

            # Create new order
            order = Order.objects.create(
                status="CREATED",
                total_amount=0,
                user=user
            )

            # Extract order items from the request
            items = validated_data['items']
            total_price = 0

            for item in items:
                try:
                    # Fetch the product item:
                    try:
                        product = Product.objects.select_for_update().get(id=item['product_id'])

                    except Product.DoesNotExist:
                        raise ValueError(
                            f"Product {item['product_id']} not found"
                        )

                    # Update the product quantity
                    StockUpdateService.decrease_quantity(product.id, item['quantity'])
                    item_price = product.price * item['quantity']

                    # Create new order item object
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],

                    )

                    # Increase the order total price
                    total_price += item_price
                except Product.DoesNotExist:
                    raise ValueError()

            order.total_amount = total_price
            order.status = "CREATED"
            order.save()
            return order
        except User.DoesNotExist:
            raise ValueError()

