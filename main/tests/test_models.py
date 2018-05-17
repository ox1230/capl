from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Category, History
from main.process import Processing

from datetime import date
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class HistoryModelTest(TestCase):
    
    def test_get_absolute_url_from_history(self):
        cate =  Category.objects.create(name = '첫번째분류')
        hist = History.objects.create(category = cate)
        self.assertEqual(hist.get_absolute_url(), '/add_history/')
    
    def test_can_insert_History_well(self):
        cate =  Category.objects.create(name = '첫번째분류')
        
        name= "test"
        price = 2000
        written_date = date(2018,1,1)

        History.objects.create(category = cate ,name = name, price = price, written_date = written_date)

        hist = History.objects.first()

        self.assertEqual(hist.category ,cate)
        self.assertEqual(hist.name , name)
        self.assertEqual(hist.price, price)
        self.assertEqual(hist.written_date , written_date)



class CategoryModelTest(TestCase):
    def test_can_insert_category_well(self):
        name = "첫번째"
        assigned = 100000
        Category.objects.create(name = name, assigned = assigned)

        cate = Category.objects.first()

        self.assertEqual(cate.assigned , assigned)
        self.assertEqual(cate.name , name)
        
        

        