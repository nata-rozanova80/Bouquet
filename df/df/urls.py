
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),

    path('catalog/', include('catalog.urls')),  # Подключаем маршруты приложения catalog
    path('users/', include('users.urls')),  # Подключение пользователей
    path('orders/', include('orders.urls')),  # Подключаем приложение orders
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)