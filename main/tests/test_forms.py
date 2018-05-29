from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Category, History, HalbuHistory
from main.process import Processing
from main.forms import HistoryForm

from datetime import date
from unittest import skip
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class HistoryFormTest(TestCase):
    
    @skip
    def test_form_html(self):
        form = HistoryForm()
        self.fail(form.as_p())

    def test_form_item_input_has_css_classes(self):
        form = HistoryForm()
        
        self.assertIn('class="form-control input"',form.as_p())
        self.assertIn('select',form.as_p())

    def test_form_validation_for_blank(self):
        cate = Category.objects.create()
        form = HistoryForm(data = {'name':'', 'category':cate.id, 'price':1000, 'written_date': date.today()})
        self.assertTrue(form.is_valid())

        form = HistoryForm(data = {'name':'', 'category':None, 'price':1000, 'written_date': date.today()})
        self.assertFalse(form.is_valid())

        form = HistoryForm(data = {'name':'', 'category':cate.id, 'price':None ,'written_date': date.today()})
        self.assertFalse(form.is_valid())

 
    def test_form_save_handles_saving_to_a_list(self):
        cate = Category.objects.create()
        
        form = HistoryForm(data = {'name':'hihi', 'category':cate.id, 'price':1000, 'written_date': date.today()})
        new_history = form.save()
        self.assertEqual(new_history, History.objects.first())
        self.assertEqual(new_history.name, 'hihi')
        self.assertEqual(new_history.category , cate)
        self.assertEqual(new_history.price ,1000)
        self.assertEqual(new_history.written_date ,date.today())
    
    def test_form_save_history_and_halbu_well(self):
        cate = Category.objects.create()
        
        form = HistoryForm(data = {'name':'hihi', 'category':cate.id, 'price':2400, 'written_date': date.today(), 
        'halbu_week': 3})

        new_history = form.save()
        halbu = HalbuHistory.objects.first()

        self.assertEqual(new_history, History.objects.first())
        self.assertEqual(new_history.name, 'hihi')
        self.assertEqual(new_history.category , cate)
        self.assertEqual(new_history.price ,2400)
        self.assertEqual(new_history.written_date ,date.today())

        self.assertEqual(halbu.category, cate)
        self.assertEqual(halbu.history, new_history)
        self.assertEqual(halbu.depre, 800)

        