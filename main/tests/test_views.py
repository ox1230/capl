from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page,show_history, NORMAL_DATE_FORMAT, WITHOUT_WEEKDAY_DATE_FORMAT
from main.models import Category, History
from main.process import Processing, CategoryInfo
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


    def test_home_page_returns_correct_html_first(self):        
        cate = Category.objects.create(name = 'test', assigned = 100000)

        
        request = HttpRequest()      # 사용자가 보낸 요청 확인
        response = home_page(request)   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        

        expected_html = render_to_string('home.html', request = request, context = 
        {
            'today_date': date.today().strftime(NORMAL_DATE_FORMAT),   #현재시간이 나오는지까지 확인
            'total_sum': 0 ,
            'residual': 100000,
            'list_of_category_info': [CategoryInfo(cate)],
        })
        
        self.assertEqual(remove_csrf_tag(response.content.decode()),remove_csrf_tag(expected_html))
    
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
    
    def test_show_history_returns_correct_html(self):        
        cate = Category.objects.create(name = 'test', assigned = 100000)

        this_week_history = History.objects.create(category= cate, price = 2700, name = "first_item" ,written_date = date.today() )
        ago_history = History.objects.create(category= cate, price = 2000, name = "second_item" ,written_date = date.today() + timedelta(days = -7)  )
        
             # 사용자가 보낸 요청 확인
        request = HttpRequest()
        response =  self.client.get("/show_history/")   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        

        expected_html = render_to_string('show_history.html', request = request, context = 
        {
            'this_week_history' : {this_week_history: this_week_history.written_date.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)},
            'long_ago_history' : {ago_history: ago_history.written_date.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)},
        })
        
        self.assertEqual(remove_csrf_tag(response.content.decode()),remove_csrf_tag(expected_html))

        self.assertContains(response, "first_item")
        self.assertContains(response, "second_item")

    def test_delete_history_delete_it_and_returns_correct_html(self):
        cate = Category.objects.create(name = 'test', assigned = 100000)

        hist = History.objects.create(category= cate, price = 2700, name = "first_item" ,written_date = date.today() )

        response = self.client.post('/delete_history',data ={"id" : hist.id})

        filt = History.objects.filter(id = hist.id)

        self.assertNotIn(hist,filt)        
        
        self.assertRedirects(response, '/show_history/')
