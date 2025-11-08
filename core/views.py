# Стандартные библиотеки
import json

# Django
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, F, Prefetch
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone

# Приложения
from .models import Order, Product, Review
from .forms import ReviewForm, OrderForm
from .data import * 


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, является ли пользователь сотрудником (is_staff).
    Если проверка не пройдена, пользователь перенаправляется на главную страницу
    с сообщением об ошибке.
    """

    def test_func(self):
        """Проверяет, аутентифицирован ли пользователь и является ли сотрудником."""
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        """Обрабатывает отсутствие прав доступа, показывая сообщение об ошибке."""
        messages.error(self.request, "У вас нет доступа к этому разделу.")
        return redirect("landing")
    
class Custom404View(TemplateView):
    template_name = '404.html'


class LandingView(TemplateView):
    template_name = 'core/landing.html'

class ThanksView(TemplateView):
    template_name = 'core/thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        source = self.kwargs.get('source')
        context['source'] = source 

        context['additional_message'] = 'Спасибо, что выбрали нас!'

        if source == 'order':
            context['source_message'] = "Ваш заказ успешно создан и принят в обработку"
        elif source == 'review':
            context['source_message'] = "Ваш отзыв успешно отправлен и будет опубликован после модерации"
        elif source:
            context['source_message'] = f"Благодарим вас за ваше действие, инициированное со страницы: {source}."
        else:
            context['source_message'] = "Спасибо за посещение!"

        return context



class OrdersListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 4

    def test_func(self):
        # Только для персонала
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет доступа к этой странице.")
        return redirect("landing")

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "").strip()
        check_boxes = self.request.GET.getlist("search_in") or ['name']

        if not search_query:
            return queryset

        filters = Q()

        if "phone" in check_boxes:
            filters |= Q(phone__icontains=search_query)

        if "name" in check_boxes:
            filters |= Q(client_name__icontains=search_query)

        if "status" in check_boxes:
            matching_status_codes = [
                code for code, display in Order.STATUS_CHOICES
                if search_query.lower() in display.lower()
            ]
            if matching_status_codes:
                filters |= Q(status__in=matching_status_codes)
            else:
                filters |= Q(status__icontains=search_query)

        return queryset.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список заказов'
        return context


class OrderDetailView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    pk_url_kwarg = 'order_id'


class OrderConfirmView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.status = 'confirmed'
        order.save()
        return redirect('order_detail', order_id=order.id)

class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.status = 'cancelled'
        order.save()
        return redirect('order_detail', order_id=order.id)

class ProductListView(ListView):
    model = Product
    template_name = 'core/products.html'
    context_object_name = "products"


class ProductsDetailView(DetailView):
    """
    Представление для отображения детальной информации о продукте.
    Используется модель Product и явно указанное имя шаблона
    """
    model = Product
    template_name = 'core/product_detail.html'


class ReviewsListView(ListView):
    model = Review
    template_name = 'core/reviews.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']

    def get_queryset(self):
        return Review.objects.filter(is_published=True).order_by('-created_at')

class AboutMilkView(TemplateView):
    template_name = 'core/about_milk.html'

class DeliveryPaymentView(TemplateView):
    template_name = 'core/delivery_payment.html'


class ReviewCreateView(CreateView):
    """
    Представление для создания нового отзыва.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'core/reviews_form.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.is_published = False
        review.save()
        messages.success(self.request, f"Отзыв от {review.client_name} успешно отправлен на модерацию!")
        return redirect("thanks_with_source", source='review')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    

    
        

class OrderCreateView(CreateView):
    def get(self, request):
        form = OrderForm()
        products = Product.objects.all()
        return render(request, 'core/order_form.html', {
            "form": form,
            "products": products,
            "form_data": {},
        })

    def post(self, request):
        form = OrderForm(request.POST)
        products = Product.objects.all()

        if form.is_valid():
            selected_products = request.POST.getlist("product")
            product_quantities = {}

            for pid in selected_products:
                try:
                    qty = int(request.POST.get(f'quantity_{pid}', '1'))
                    if qty > 0:
                        product_quantities[pid] = qty
                except ValueError:
                    continue

            if not product_quantities:
                return render(request, 'core/order_form.html', {
                    "form": form,
                    "products": products,
                    "error": "Выберите хотя бы один товар и укажите количество.",
                    "form_data": request.POST,
                })

            order = form.save(commit=False)
            order.appointment_date = timezone.now()
            order.product_quantities = json.dumps(product_quantities)
            order.save()
            order.products.set(product_quantities.keys())

            messages.success(request, f"Ваш заказ успешно создан, {order.client_name}!")
            return redirect("thanks_with_source", source='order')

        return render(request, 'core/order_form.html', {
            "form": form,
            "products": products,
            "form_data": request.POST,
        })