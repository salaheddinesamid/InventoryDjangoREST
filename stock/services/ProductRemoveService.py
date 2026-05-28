from ..models import Product


class ProductRemoveService:
    @staticmethod
    def remove_product(id):
        product_exists = Product.objects.filter(
            id=id
        ).exists()

        if not product_exists:
            raise Product.DoesNotExist()

        Product.objects.get(
            id=id
        ).delete()
