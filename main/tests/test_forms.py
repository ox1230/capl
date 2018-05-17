from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Category, History
from main.process import Processing
from main.forms import HistoryForm

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

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = HistoryForm()
        
        self.assertIn('class="form-control input-lg"',form.as_p())
        self.assertIn('select',form.as_p())
    
    @skip
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data = {'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'], [EMPTY_LIST_ERROR] )
    
    @skip
    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data = {'text':'do me'})
        new_item = form.save(for_list = list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)
        
        

        