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
    })

def add_history_page(request:HttpRequest):
    return render(request, 'add_history.html',{
        'category_list' : Category.objects.all(),
    })

def add_history_action(request:HttpRequest):
    
    new_history = History()
    new_history.name = request.POST['history_name']
    #아직은 카테고리가 없으면 추가
    
    name = request.POST['history_category']
    if  Category.objects.filter(name = name).count() == 0:
        Category.objects.create(name = name)
    new_history.category = Category.objects.get(name = name)
    new_history.price = int(request.POST['history_price'])
    new_history.save()
    
    
    Processing.total_sum += new_history.price
    Processing.residual -= new_history.price

    return redirect('main/')