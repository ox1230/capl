from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from capl.process import Processing
from main.models import History, Category
# Create your views here.

def home_page(request:HttpRequest):
    
    return render(request, 'home.html',
    {
        'total_sum': Processing.total_sum,
        'residual': Processing.residual,
        'categories': Category.objects.all(),
    })

def add_history_page(request:HttpRequest):
    return render(request, 'add_history.html',{
        'category_list' : Category.objects.all(),
    })

def add_history_action(request:HttpRequest):
 
    #아직은 카테고리가 없으면 추가
    cate_name = request.POST['history_category']
    if  Category.objects.filter(name =cate_name).count() == 0:
        Category.objects.create(name = cate_name)
    
    Processing.add_history(cate_name,request.POST['history_name'], int(request.POST['history_price']))

    return redirect('main/')