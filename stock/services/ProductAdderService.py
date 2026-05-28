from ..models import Product


class ProductAdderService:

    @staticmethod
    def add_product(validated_data):
        # Check if the product already exists:
        product_exists = Product.objects.filter(
            name__iexact=validated_data["name"]
        ).exists()
        if product_exists:
            raise ValueError()

        # Otherwise, create new product
        product = Product.objects.create(
            name=validated_data["name"],
            serial_number=validated_data['serial_number'],
            manufacturer=validated_data['manufacturer'],
            production_year=validated_data['production_year'],
            price=validated_data['price'],
            quantity_available=validated_data['quantity_available'],
            is_available=validated_data['is_available'],
            sale_start=validated_data['sale_start'],
            sale_end=validated_data['sale_end'],
            category=validated_data['category']
        )

        return product