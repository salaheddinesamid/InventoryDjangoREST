from django.db import models
from stock.models import Product
# Create your models here.


class Order(models.Model):
    STATUS = {
        "CREATED": "C",
        "CONFIRMED": "CF",
        "DELIVERED": "D",
        "CANCELED": "CC"
    }
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='order_items')
    quantity = models.IntegerField()
