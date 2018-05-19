from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page, NORMAL_DATE_FORMAT
from main.models import Category, History
from main.process import Processing, CategoryInfo

from datetime import date
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
    
    def test_db_reset(self):
        cate = Category.objects.create(name = 'test')

        response = self.client.get('/reset/')  

        cates = Category.objects.all()

        self.assertNotIn(cate, cates)
        self.assertEqual(cates.count(), 3)

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
        })

        saved_history = History.objects.first()

        self.assertEqual(saved_history.category ,cate_ )
        self.assertEqual(saved_history.name , '거래내역내용')
        self.assertEqual(saved_history.price , 1000)

        self.assertRedirects(response, '/main/')


        