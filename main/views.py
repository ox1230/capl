from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .process import Processing
from main.models import History, Category
from main.forms import HistoryForm
# Create your views here.

def root(request:HttpRequest):
    return redirect('main')

def home_page(request:HttpRequest):
    
    return render(request, 'home.html',
    {
        'total_sum': Processing.get_total_sum(),
        'residual': Processing.get_total_residual(),
        'categories': Category.objects.all(),
    })

def add_history(request:HttpRequest):
    form = HistoryForm()
    if request.method == 'POST':
        form = HistoryForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')


    return render(request, 'add_history.html',{
        'add_history_form' : form,
    })