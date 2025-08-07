from django.contrib import admin
from .models import Review, Product, Order



# Остальные модели
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Order)

