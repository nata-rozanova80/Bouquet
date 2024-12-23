# df/orders/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_status_update

@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    if not created:
        send_status_update(instance.user, instance.id, instance.status)
