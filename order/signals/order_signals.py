from ..models import Order
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Order)
def post_create(sender, instance, created, **kwargs):
    print("An order has been created...")
