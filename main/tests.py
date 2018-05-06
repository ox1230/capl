from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from capl.process import Processing
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)
    

class MainViewTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        response = self.client.get('', data =  {
            'total_sum': Processing.total_sum , 'residual': Processing.residual
        })  

        self.assertTemplateUsed(response, 'home.html')

    

    def test_home_page_returns_correct_html_first(self):        

        
        request = HttpRequest()      # 사용자가 보낸 요청 확인
        response = home_page(request)   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        
        expected_html = render_to_string('home.html', request = request, context = 
        {
            'total_sum': Processing.total_sum , 'residual': Processing.residual
        })
        
        self.assertEqual(remove_csrf_tag(response.content.decode()),remove_csrf_tag(expected_html))




class AddhistoryTest(TestCase):
    def test_add_history_url_resolve_add_history_page_correctly(self):
        response = self.client.get('/add_history/')  

        self.assertTemplateUsed(response, 'add_history.html')

        
    def test_can_process_a_add_history_POST_request_and_go_main(self):
        
        present_total_sum = Processing.total_sum
        present_residual = Processing.residual

        response = self.client.post(
            '/add_history',
            data = {'history_category': '거래내역항목',
                    'history_name' : '거래내역내용',
                    'history_price' : 100
        })

        self.assertEqual(Processing.total_sum, present_total_sum + 100)
        self.assertEqual(Processing.residual, present_residual - 100)
        
        self.assertRedirects(response, '/main/')
        
