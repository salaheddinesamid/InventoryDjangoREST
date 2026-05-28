from ..models import Product
from django.db import transaction


class StockUpdateService:

    @staticmethod
    @transaction.atomic
    def update_product(product_id, validated_data):
        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            raise ValueError("Product not found")

        # Prevent duplicate names
        if "name" in validated_data:

            existing_product = Product.objects.filter(
                name__iexact=validated_data["name"]
            ).exclude(id=product_id).exists()

            if existing_product:
                raise ValueError(
                    "Product with this name already exists"
                )

            product.name = validated_data["name"]

        # Update price
        if "price" in validated_data:

            if validated_data["price"] <= 0:
                raise ValueError(
                    "Price must be greater than zero"
                )

            product.price = validated_data["price"]

        # Update quantity
        if "quantity_available" in validated_data:

            if validated_data["quantity_available"] < 0:
                raise ValueError(
                    "Quantity cannot be negative"
                )

            product.quantity_available = validated_data[
                "quantity_available"
            ]

        product.save()

        return product

    @staticmethod
    @transaction.atomic
    def decrease_quantity(product_id, quantity):
        try:
            product = Product.objects.select_for_update().get(id=product_id)
            product.quantity_available = product.quantity_available - quantity
            product.save()
        except Product.DoesNotExist:
            raise ValueError("Product Not Found")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if product.quantity_available < quantity:
            raise ValueError("Insufficient stock")

        return product

    @staticmethod
    @transaction.atomic
    def restore_quantity(product_id, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        try:
            product = Product.objects.select_for_update().get(id=product_id)
            product.quantity_available = product.quantity_available + quantity
            product.save()
        except Product.DoesNotExist:
            raise ValueError("Product Not Found")

        return product
