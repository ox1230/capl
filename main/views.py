from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .process import Processing
from main.models import History, Category
from main.forms import HistoryForm

from datetime import date
# Create your views here.

NORMAL_DATE_FORMAT = "%Y-%m-%d %A"

def root(request:HttpRequest):
    return redirect('main')

def home_page(request:HttpRequest):
    
    #날짜 만들기
    today =date.today()
    #category 만들기
    cates = Category.objects.exclude(assigned = None)
    resid_of_cates = {}
    for cate in cates:
        resid_of_cates[cate] = Processing.get_category_residual(cate)

    
    return render(request, 'home.html',
    {
        'today_date': today.strftime(NORMAL_DATE_FORMAT),
        'total_sum': Processing.get_total_sum(),
        'residual': Processing.get_total_residual(),
        'resid_of_cates': resid_of_cates,
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