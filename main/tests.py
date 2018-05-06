from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from capl.process import Processing
import re

# Create your tests here.

class MainViewTest(LiTestCase):
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
        
        self.assertEqual(self.remove_csrf_tag(response.content.decode()), self.remove_csrf_tag(expected_html))



    def remove_csrf_tag(self,text):
        """Remove csrf tag from TEXT"""
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)