from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Category, History
from capl.process import Processing
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class MainAndItemModelTest(TestCase):
    
    def test_processing_add_history(self):
        Category.objects.create(name = '첫번째분류')
        
        cate = Category.objects.first()

        self.assertEqual("첫번째분류", cate.name)
        self.assertEqual(100000, cate.residual)

        Processing.add_history("첫번째분류","거래내역",1000)
        cate = Category.objects.first()
        self.assertEqual("첫번째분류", cate.name)
        self.assertEqual(99000, cate.residual)

    def test_get_absolute_url_from_history(self):
        cate =  Category.objects.create(name = '첫번째분류')
        hist = History.objects.create(category = cate)
        self.assertEqual(hist.get_absolute_url(), '/add_history/')

        
        

        