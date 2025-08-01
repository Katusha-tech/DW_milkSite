from doctest import master
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

