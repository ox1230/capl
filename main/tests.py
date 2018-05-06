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




class AddItemTest(TestCase):
    def test_add_item_url_resolve_add_item_page(self):
        response = self.client.get('/add_item/')  

        self.assertTemplateUsed(response, 'add_item.html')