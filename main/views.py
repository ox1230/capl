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

def add_history_page(request:HttpRequest):
    return render(request, 'add_history.html')

def add_history_action(request:HttpRequest):
    Processing.total_sum += int(request.POST['history_price'])
    Processing.residual -= int(request.POST['history_price'])

    return redirect('main/')