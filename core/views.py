from django.shortcuts import redirect, render
from django.http import HttpResponse
from  django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, Product, Review
from .forms import ReviewForm, OrderForm
from django.db.models import Q
import json
from django.utils import timezone
from .data import * 

def base(request):
    return render(request, 'base.html')

def landing(request):
    return render(request, 'core/landing.html')

def thanks(request):
    return render(request, 'core/thanks.html')


@login_required
def orders_list(request):
    if not request.user.is_staff:
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect("landing")
    
    all_orders = Order.objects.all()
    search_query = request.GET.get('search', None)
    check_boxes = request.GET.getlist('search_in')
    
    if not check_boxes:
        check_boxes = ['name']

    if search_query:
        filters = Q()
        
        if "phone" in check_boxes:
            filters |= Q(phone__icontains=search_query)

        if "name" in check_boxes:
            filters |= Q(client_name__icontains=search_query)

        if "status" in check_boxes:
            # Поиск по отображаемым значениям статуса
            status_display_map = dict(Order.STATUS_CHOICES)
            matching_status_codes = []
            
            # Ищем коды статусов, у которых отображаемое значение содержит поисковый запрос
            for code, display in Order.STATUS_CHOICES:
                if search_query.lower() in display.lower():
                    matching_status_codes.append(code)
            
            # Если найдены совпадения, добавляем их в фильтр
            if matching_status_codes:
                filters |= Q(status__in=matching_status_codes)
            else:
                # Если нет совпадений по отображаемым значениям, 
                # пробуем искать по коду статуса (для администраторов)
                filters |= Q(status__icontains=search_query)

        all_orders = all_orders.filter(filters)

    context = {
        'title': 'Список заказов',
        'orders': all_orders,
    }
    return render(request, 'core/orders_list.html', context)


@login_required
def order_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    context = {'title': f'Заказ №{order_id}', 'order': order}
    return render(request, 'core/order_detail.html', context)

@login_required
def order_confirm(request, order_id):
    """Логика подтверждения заказа"""
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.status = 'confirmed'  # или 'confirmed' — зависит от твоей модели
        order.save()
    return redirect('order_detail', order_id=order.id)

@login_required
def order_cancel(request, order_id):
    """Логика отмены заказа"""
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.status = 'cancelled'  # или 'cancelled'
        order.save()
    return redirect('order_detail', order_id=order.id)

def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'core/products.html', context)

def reviews(request):
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    context = {
        'reviews': reviews,
    }
    return render(request, 'core/reviews.html', context)

def about_milk(request):
    return render(request, 'core/about_milk.html')

def delivery_payment(request):
    return render(request, 'core/delivery_payment.html')


def create_review(request):
    if request.method == 'GET':
        form = ReviewForm()
        context = {
            'title': 'Создание отзыва',
            'form': form,
            'button_text': 'Создать',
        }
        return render(request, 'core/reviews_form.html', context)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)
            review.is_published = False
            review.save()

            client_name = form.cleaned_data.get('client_name')
            messages.success(request, f"Отзыв от {client_name} успешно создан и отправлен на модерацию!")

            return redirect("thanks")
        else:
            # Форма не прошла валидацию — нужно вернуть шаблон с ошибками
            context = {
                'title': 'Создание отзыва',
                'form': form,
                'button_text': 'Создать',
            }
            return render(request, 'core/reviews_form.html', context)
        

def create_order(request):
    products = Product.objects.all()

    if request.method == 'GET':
        form = OrderForm()
        return render(request, 'core/order_form.html', {
            "form": form,
            "products": products,
            "form_data": {},
        })

    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Получаем выбранные продукты и их количество
            selected_products = request.POST.getlist("product")
            product_quantities = {}
            for pid in selected_products:
                qty = request.POST.get(f'quantity_{pid}', '1')
                try:
                    qty = int(qty)
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

            order.product_quantities = json.dumps(product_quantities)
            order.save()
            order.products.set(product_quantities.keys())

            order = form.save(commit=False)
            order.appointment_date = timezone.now()
            order.save()

            messages.success(request, f"Ваш заказ успешно создан, {order.client_name}!")
            return redirect('thanks')

        return render(request, 'core/order_form.html', {
            "form": form,
            "products": products,
            "form_data": request.POST,
        })