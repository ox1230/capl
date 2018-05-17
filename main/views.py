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

    if request.method == 'POST':
    #아직은 카테고리가 없으면 추가
        cate_id = request.POST['history_category']
        if  Category.objects.filter(id =cate_id).count() == 0:
            Category.objects.create(id = cate_id)
        
        Processing.add_history(cate_id,request.POST['history_name'], int(request.POST['history_price']))
        return redirect('main')
    
    else:
        return render(request, 'add_history.html',{
            'add_history_form' : HistoryForm(),
        })