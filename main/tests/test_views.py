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
    

class MainViewTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        Category.objects.create(name = 'test')
       
        response = self.client.get('', data =  {
            'total_sum': Processing.total_sum , 
            'residual': Processing.residual,
            'categories' : Category.objects.all(),
        })  

        self.assertTemplateUsed(response, 'home.html')

    

    def test_home_page_returns_correct_html_first(self):        
        Category.objects.create(name = 'test')

        
        request = HttpRequest()      # 사용자가 보낸 요청 확인
        response = home_page(request)   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        
        expected_html = render_to_string('home.html', request = request, context = 
        {
            'total_sum': Processing.total_sum ,
             'residual': Processing.residual,
             'categories' : Category.objects.all(),
        })
        
        self.assertEqual(remove_csrf_tag(response.content.decode()),remove_csrf_tag(expected_html))




class AddhistoryTest(TestCase):
    def test_add_history_url_resolve_add_history_page_correctly(self):

        Category.objects.create(name = '첫번째')
        Category.objects.create(name = '거래내역분류')  #카테고리 확인용
        
        response = self.client.get('/add_history/')  

        self.assertTemplateUsed(response, 'add_history.html')

        self.assertContains(response,'첫번째')
        self.assertContains(response,'거래내역분류' )


        
    def test_can_save_and_process_add_history_POST_request_and_go_main(self):
        
        cate_ = Category.objects.create(name = '거래내역분류')
        self.assertEqual(cate_.residual, 100000)

        present_total_sum = Processing.total_sum
        present_residual = Processing.residual

        response = self.client.post(
            '/add_history/',
            data = {'history_category': cate_.name,
                    'history_name' : '거래내역내용',
                    'history_price' : 1000,
        })

        saved_history = History.objects.first()

        self.assertEqual(saved_history.category ,cate_ )
        self.assertEqual(saved_history.name , '거래내역내용')
        self.assertEqual(saved_history.price , 1000)

        self.assertEqual(Processing.total_sum, present_total_sum + 1000)
        self.assertEqual(Processing.residual, present_residual - 1000)
        
        cate_ = Category.objects.get(name = '거래내역분류')
        self.assertEqual(cate_.residual, 100000 - 1000)

        self.assertRedirects(response, '/main/')


        