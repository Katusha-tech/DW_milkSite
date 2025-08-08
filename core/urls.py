# core/urls.py
from django.contrib import admin
from django.urls import path
from .views import (ThanksView, 
                    ProductListView,
                    ProductsDetailView,
                    OrdersListView, 
                    OrderDetailView, 
                    OrderConfirmView, 
                    OrderCancelView, 
                    ReviewsListView, 
                    ReviewCreateView, 
                    OrderCreateView, 
                    AboutMilkView, 
                    DeliveryPaymentView)

# Маршруты доступны с префиксом /milksite/
urlpatterns = [
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('thanks/<str:source>/', ThanksView.as_view(), name='thanks_with_source'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:order_id>/confirm/', OrderConfirmView.as_view(), name='order_confirm'),
    path('orders/<int:order_id>/cancel/', OrderCancelView.as_view(), name='order_cancel'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product_detail'),
    path('reviews/', ReviewsListView.as_view(), name='reviews'),
    path('create_review/', ReviewCreateView.as_view(), name='create_review'),
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
    path('about_milk/', AboutMilkView.as_view(), name='about_milk'),
    path('delivery_payment/', DeliveryPaymentView.as_view(), name='delivery_payment'),
] 