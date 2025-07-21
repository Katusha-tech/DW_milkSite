from django.shortcuts import render
from django.http import HttpResponse
from .data import * 

def main(request):
    return HttpResponse('Добро пожаловать на MilkSite!')

def thanks(request):
    return render(request, 'core/thanks.html', context)

def orders_list(request):
    context = {
        'orders': orders, 'title': 'Список заказов'
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id: int):
    try:
        order = [o for o in orders if o['id'] == order_id][0]
    except IndexError:
        return HttpResponse(status=404)
    context = {'title': f'Заказ №{order_id}', 'order': order}
    return render(request, 'core/order_detail.html', context)



