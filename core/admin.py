from django.contrib import admin
from .models import Review, Product, Order



# Остальные модели
admin.site.register(Review)
admin.site.register(Product)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'status', 'delivery_day')
    list_filter = ('client_name', 'status', 'delivery_day')
    search_fields = ('client_name', 'phone')
    ordering = ('client_name',)

admin.site.register(Order, OrderAdmin)