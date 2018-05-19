from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .process import db_reset, Processing
from main.models import History, Category
from main.forms import HistoryForm

from datetime import date
# Create your views here.

NORMAL_DATE_FORMAT = "%Y-%m-%d %A"

def root(request:HttpRequest):
    return redirect('main')

def reset(request : HttpRequest):
    db_reset()

    return redirect('main')

def home_page(request:HttpRequest):
    
    today =date.today()
    infos_of_main = Processing.get_informations_for_main()

    return render(request, 'home.html',
    {
        'today_date': today.strftime(NORMAL_DATE_FORMAT),
        'total_sum': infos_of_main['total_sum'],
        'residual': infos_of_main['total_residual'],
        'list_of_category_info': infos_of_main['list_of_category_info'],
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