from django import db
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Отзывы
class Review(models.Model):
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(verbose_name="Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв от {self.client_name}. Статус: {'Опубликован' if self.is_published else 'Не опубликован'}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['is_published']),
        ]

# Продукт
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга", blank=True)
    image = models.ImageField(upload_to="images/products/", blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['is_popular']),
        ]

# Заказ
class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("confirmed", "Подтвержденная"),
        ("cancelled", "Отменённая"),
        ("completed", "Выполненная"),
    ]

    DELIVERY_DAY_CHOICES = [
        ("Вторник", "Вторник"),
        ("Пятница", "Пятница"),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=25, default="", verbose_name="Телефон")
    comment = models.TextField(max_length=100, blank=True, db_index=True, verbose_name="Комментарий")
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    appointment_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата заказа")
    delivery_day = models.CharField(max_length=20, choices=DELIVERY_DAY_CHOICES, default="Вторник",verbose_name="День привоза")

    def __str__(self):
        return f"Заказ {self.id}: {self.client_name}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=['client_name']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['date_created']),
            models.Index(fields=['status', 'appointment_date'], name='status_appointment_date_idx'),
            models.Index(fields=['client_name', 'phone'], name='client_name_phone_idx'),
        ]

# Промежуточная модель — товар в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"