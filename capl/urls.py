"""capl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.root, name = "root"),
    path('reset/', views.reset, name= "reset"),
    path('first/', views.first, name = "first"),
    path('main/', views.home_page, name= "main"),
    path('add_history/', views.add_history, name = "add_history"),
    path('show_history/', views.show_history, name = "show_history"),
    path('delete_history', views.delete_history , name = "delete_history" ),
    path('admin/', admin.site.urls),
]
