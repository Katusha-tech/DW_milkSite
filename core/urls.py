# core/urls.py
from django.contrib import admin
from django.urls import path
from .views import thanks, orders_list, order_detail, order_confirm, order_cancel, products,reviews, create_review, about_milk, delivery_payment

# Маршруты доступны с префиксом /milksite/
urlpatterns = [
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/<int:order_id>/confirm/', order_confirm, name='order_confirm'),
    path('orders/<int:order_id>/cancel/', order_cancel, name='order_cancel'),
    path('products/', products, name='products'),
    path('reviews/', reviews, name='reviews'),
    path('create_review/', create_review, name='create_review'), 
    path('about_milk/', about_milk, name='about_milk'),
    path('delivery_payment/', delivery_payment, name='delivery_payment'),
] 