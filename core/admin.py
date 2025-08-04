from django.contrib import admin
from .models import Review, Product, Order, OrderItem

# Inline для отображения OrderItem внутри заказа
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']
    readonly_fields = ['get_total_price']
    fields = ['product', 'quantity', 'get_total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = "Сумма"

# Настройка Order с отображением OrderItem
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'phone', 'status', 'date_create']
    list_filter = ['status', 'date_create']
    search_fields = ['client_name', 'phone']
    inlines = [OrderItemInline]

# Остальные модели
admin.site.register(Review)
admin.site.register(Product)

