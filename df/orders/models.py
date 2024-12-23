# orders/models.py

#import Order
from django.db import models
from django.conf import settings
from users.models import User
from catalog.models import Product



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),

    ]

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.IntegerField()  # Telegram User ID
    products = models.ManyToManyField(Product, through='OrderItem')
    # bouquet = models.CharField(max_length=255)
    # address = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ожидает')


    # Поля для доставки:
    recipient_name = models.CharField(max_length=100, blank=True, verbose_name='Имя получателя')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name='Заказ')
    status = models.CharField(max_length=10, choices=Order.STATUS_CHOICES, verbose_name='Новый статус')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Изменил')

    def __str__(self):
        return f"Заказ #{self.order.id}: {self.get_status_display()} в {self.changed_at}"

class Meta:
    ordering = ['-created_at']
