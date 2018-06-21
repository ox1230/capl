from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page,show_history, NORMAL_DATE_FORMAT, WITHOUT_WEEKDAY_DATE_FORMAT
from main.models import Category, History
from main.process import Processing, CategoryInfo , WeekAndDay
from datetime import date, timedelta

from unittest import skip
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)
    

class MainViewTest(TestCase):

    def test_root_url_resolves_to_main_url(self):
        Category.objects.create(name = 'test')
       
        response = self.client.get('', data =  {
            'total_sum':1000 , 
            'residual': 2000,
        })  

        self.assertRedirects(response, '/main/')
    
    def test_db_reset_page(self):
        cate = Category.objects.create(name = 'test')

        response = self.client.get('/reset/')  

        cates = Category.objects.all()

        self.assertNotIn(cate, cates)
        self.assertEqual(cates.count(), 4)

        self.assertRedirects(response, '/main/')


class AddhistoryTest(TestCase):
    def test_add_history_url_resolve_add_history_page_correctly(self):

        Category.objects.create(name = '첫번째')
        Category.objects.create(name = '거래내역분류')  #카테고리 확인용
        
        response = self.client.get('/add_history/')  

        self.assertTemplateUsed(response, 'add_history.html')

        self.assertContains(response,'첫번째')
        self.assertContains(response,'거래내역분류')


    def test_can_save_and_process_add_history_POST_request_and_go_main(self):
        
        cate_ = Category.objects.create(name = '거래내역분류')
 
        response = self.client.post(
            '/add_history/',
            data = {'category': cate_.id,
                    'name' : '거래내역내용',
                    'price' : '1000',
                    'written_date': date.today(),
        })

        saved_history = History.objects.first()

        self.assertEqual(saved_history.category ,cate_ )
        self.assertEqual(saved_history.name , '거래내역내용')
        self.assertEqual(saved_history.price , 1000)
        self.assertEqual(saved_history.written_date , date.today())

        self.assertRedirects(response, '/main/')


class ShowHistoryTest(TestCase):

    def test_delete_history_delete_it_and_returns_correct_html(self):
        cate = Category.objects.create(name = 'test', assigned = 100000)

        hist = History.objects.create(category= cate, price = 2700, name = "first_item" ,written_date = date.today() )

        response = self.client.post('/delete_history',data ={"id" : hist.id})

        filt = History.objects.filter(id = hist.id)

        self.assertNotIn(hist,filt)        
        
        self.assertRedirects(response, '/show_history/')
