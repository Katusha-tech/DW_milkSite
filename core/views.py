from django.shortcuts import render
from django.http import HttpResponse
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from .data import * 

def base(request):
    return render(request, 'base.html')

def landing(request):
    return render(request, 'core/landing.html')

def thanks(request):
    return render(request, 'core/thanks.html')

def orders_list(request):
    context = {
        'orders': ORDERS, 'title': 'Список заказов'
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id: int):
    try:
        order = [o for o in ORDERS if o['id'] == order_id][0]
    except IndexError:
        return HttpResponse(status=404)
    context = {'title': f'Заказ №{order_id}', 'order': order}
    return render(request, 'core/order_detail.html', context)

def products(request):
    context = {
        'products': PRODUCTS, 'title': 'Продукты'
    }
    return render(request, 'core/products.html', context)

def reviews(request):
    return render(request, 'core/reviews.html')

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

