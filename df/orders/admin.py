# orders/admin.py

from django.contrib import admin
from .models import Order, OrderItem
from .models import OrderStatusHistory


# Важно: должно наследоваться от admin.TabularInline или admin.StackedInline
class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'changed_at', 'changed_by')
    can_delete = False
    verbose_name = "История статусов"
    verbose_name_plural = "Истории статусов"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'status')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'recipient_name', 'phone', 'address', 'comment')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [OrderStatusHistoryInline]

# Переопределение метода save_model для записи изменений статуса
    def save_model(self, request, obj, form, change):
        if change:
            # Получаем предыдущее состояние заказа
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # Создаем запись в истории изменений
                OrderStatusHistory.objects.create(
                    order=obj,
                    status=obj.status,
                    changed_by=request.user
                )
        super().save_model(request, obj, form, change)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')

class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_at', 'changed_by')
    list_filter = ('status', 'changed_at')
    search_fields = ('order__id', 'changed_by__username')

# Регистрация моделей в админке
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderStatusHistory, OrderStatusHistoryAdmin)


