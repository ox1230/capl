from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from capl.process import Processing
# Create your views here.

def home_page(request:HttpRequest):
    return render(request, 'home.html',
    {
        'total_sum': Processing.total_sum,
        'residual': Processing.residual,
    })

def add_item(request:HttpRequest):
    return render(request, 'add_item.html')