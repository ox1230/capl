from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Category, History
from main.process import Processing
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class ProcessingTest(TestCase):
    
    def test_can_process_total_assigned(self):
        Category.objects.create(name ="1", assigned = 1000)
        Category.objects.create(name ="2", assigned = 1500)
        Category.objects.create(name ="3", assigned = 1000)

        self.assertEqual(Processing.get_total_assigned(), 3500)
    
    def test_can_process_total_residual(self):
        cate = Category.objects.create(name ="1", assigned = 1000)
        Category.objects.create(name ="2", assigned = 1500)
        
        History.objects.create(category = cate, name="1", price = 600)

        self.assertEqual(Processing.get_total_assigned(), 2500)
        self.assertEqual(Processing.get_total_residual(), 1900)
    
    def test_can_process_each_categories_residual(self):
        cate1 = Category.objects.create(name ="1", assigned = 10000)
        cate2 = Category.objects.create(name ="2", assigned = 10000)
        
        History.objects.create(category = cate1, name="1", price = 6000)
        
        self.assertEqual(Processing.get_category_residual(cate1), 4000)
        self.assertEqual(Processing.get_category_residual(cate2), 10000)
