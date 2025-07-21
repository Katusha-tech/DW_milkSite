# core/urls.py
from django.contrib import admin
from django.urls import path
from .views import thanks, orders_list, order_detail

# Маршруты доступны с префиксом /milksite/
urlpatterns = [
    path('thanks/', thanks),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id/>', order_detail, name='order_detail'),
]