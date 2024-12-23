# main/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import register
from .views import index

urlpatterns = [

    # Другой формат записи. Введен после ошибки перенаправления после входа
    path('', index, name='index'),  # Главная страница

    # Страница регистрации
    path('register/', register, name='register'),

    # Страница входа (используем стандартную форму Django)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Страница выхода (используем стандартную Django-форму)
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('users/', include('users.urls')),


]


