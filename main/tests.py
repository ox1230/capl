from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
import re

# Create your tests here.

class MainViewTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
       
        self.assertEqual(found.func, home_page)
    

    def test_home_page_returns_correct_html_first(self):
        request = HttpRequest()      # 사용자가 보낸 요청 확인
        response = home_page(request)   # 이것을 뷰 home_page에 전달     리턴값: HttpResponse
        
        total_sum = 0
        residual = 300000

        expected_html = render_to_string('home.html', request = request, using = 
        {
            'total_sum': 0, 'residual': 300000
        })
        
        self.assertEqual(self.remove_csrf_tag(response.content.decode()), self.remove_csrf_tag(expected_html))
    

    def remove_csrf_tag(self,text):
        """Remove csrf tag from TEXT"""
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)