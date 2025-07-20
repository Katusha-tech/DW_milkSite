from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return HttpResponse('Добро пожаловать на MilkSite!')

def thanks(request):
    return render(request, 'thanks.html')



