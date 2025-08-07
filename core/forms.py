# Импорт служебных объектов Form
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from django.forms import inlineformset_factory
from .models import Product, Review, Order, OrderItem
from django.utils.timezone import now

class ProductForm(forms.ModelForm):
    # Расширим инициализатор для добавления form-control к полям формы

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы (кроме чекбоксов)
        for field_name, field in self.fields.items():
            if field_name != "is_popular":  # Пропускаем чекбокс
                field.widget.attrs.update({"class": "form-control"})
            else:  # Для чекбокса добавляем класс переключателя
                field.widget.attrs.update({"class": "form-check-input"})

    # Валидатор поля description
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise ValidationError("Описание должно содержать не менее 10 символов.")
        return description

    class Meta:
        model = Product
        # Поля, которые будут отображаться в форме
        fields = ["name", "description", "price", "is_popular", "image"]


class OrderForm(forms.ModelForm):
    DELIVERY_DAY_CHOICES = [
        ("Вторник", "Вторник"),
        ("Пятница", "Пятница"),
    ]

    delivery_day = forms.ChoiceField(
        choices=DELIVERY_DAY_CHOICES,
        label="День привоза",
        widget=forms.Select(attrs={"class": "form-select custom-style"}),
        required=True,
    )

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-select custom-style",
            "id": "products",
            "size": "1",  # Уменьшает высоту до 1 строки
        }),
        label="Выберите продукты"
    )

    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "readonly": "readonly",
            "class": "form-control no-calendar",
            "type": "text",  # избегаем иконки календаря
            "placeholder": now().strftime("%d-%m-%Y"),
        }),
        initial=now,
        input_formats=["%d-%m-%Y"],
        label="Дата заказа"
    )

    class Meta:
        model = Order
        fields = [
            "client_name",
            "phone",
            "comment",
            "delivery_day",
            "appointment_date",
            "products",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Форматируем дату заказа
        self.fields['appointment_date'].initial = now().strftime("%d-%m-%Y")

        # Уменьшаем комментарий
        self.fields['comment'].widget.attrs.update({'rows': 3})

        # Стили для всех остальных полей (если нет вручную заданных)
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                existing_class = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing_class} form-control".strip()

class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва о мастере с использованием Bootstrap 5
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы
        for field_name, field in self.fields.items():
            if (
                field_name != "rating"
            ):  # Для рейтинга будет специальная обработка через JS
                field.widget.attrs.update({"class": "form-control"})

    # Скрытое поле для рейтинга, которое будет заполняться через JS
    rating = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
    )

    class Meta:
        model = Review
        # Исключаем поле is_published из формы для пользователей
        exclude = ["is_published"]
        widgets = {
            "client_name": forms.TextInput(
                attrs={"placeholder": "Как к вам обращаться?", "class": "form-control"}
            ),
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Расскажите что вам понравилось",
                    "class": "form-control",
                    "rows": "3",
                }
            ),
        }

