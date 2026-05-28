from django.db import models

# Create your models here.
from django.db import models


class Product(models.Model):
    PRODUCT_CATEGORY = {
        "E": "ELECTRONICS"
    }
    MANUFACTURER = {
        "Apple Inc." : "apple"
    }

    name = models.CharField(max_length=200, unique=True)
    serial_number = models.CharField(max_length=200, unique=True, null=True)
    manufacturer = models.CharField(max_length=200, choices=MANUFACTURER, null=True)
    production_year = models.IntegerField(default=0)
    price = models.FloatField()
    quantity_available = models.IntegerField(default=0)
    is_available = models.BooleanField(null=True)
    sale_start = models.DateTimeField()
    sale_end = models.DateTimeField()
    category = models.CharField(max_length=200, choices=PRODUCT_CATEGORY, null=True)


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
