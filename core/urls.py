# core/urls.py
from django.contrib import admin
from django.urls import path
from .views import thanks

# Маршруты доступны с префиксом /milksite/
urlpatterns = [
    path('thanks/', thanks),
]