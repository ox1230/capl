from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category
import unittest
import time


class VisitorTest(LiveServerTestCase):
    def setUp(self):
        """테스트 시작 전에 수행"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)   # 암묵적 대기 -- 3초
        
        #미리 설정되어 있는 데이터
        Category.objects.create(name = '군것질')
        Category.objects.create(name = '세끼')
        Category.objects.create(name = '선물')

        
    
    def tearDown(self):
        """테스트 후에 시행-- 테스트에 에러가 발생해도 실행된다"""
        self.browser.quit()
    
    def test_show_main_and_add_history(self):
        """  """
        #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Cash Planner'를 표시
        self.assertIn('Cash Planner' ,self.browser.title) 

        #메인 화면에는 현재 사용금액 정보가 있다. 현재 사용 금액은 0원이다.   -- 사용가능 금액은 300000이다.
       
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('현재 사용금액 0원', rows_text)
        self.assertIn('남은 금액 300000원', rows_text)

        # (각 category별 사용가능금액이 표시된다.)  -- 이부분 나중에 
        
        rows_text =  self.find_rows_from_table_id('detail_box')

        self.assertIn('군것질 100000원', rows_text)
        self.assertIn('세끼 100000원', rows_text)
        self.assertIn('선물 100000원', rows_text)

        #메뉴에서 거래내역추가를 눌러 거래내역 추가로 이동한다.   -- 일단 하이퍼링크로 대체
        add_history_menu = self.browser.find_element_by_id("add_history_menu")
        add_history_menu.click()

        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/add_history/')


        # edith는 식사/군것질 거래내역,  딸기바나나, 1500원을 입력한다. 
        self.browser.find_element_by_id("history_category_inputBox").send_keys('군것질')
        self.browser.find_element_by_id("history_name_inputBox").send_keys('딸기바나나')
        self.browser.find_element_by_id("history_price_inputBox").send_keys('1500')
        self.browser.find_element_by_id("add_history_button").click()
        
        
        #이어서 세끼, 짜장상회, 4000원을 입력한다.
        add_history_menu = self.browser.find_element_by_id("add_history_menu")
        add_history_menu.click()
        self.browser.find_element_by_id("history_category_inputBox").send_keys('세끼')
        self.browser.find_element_by_id("history_name_inputBox").send_keys('짜장상회')
        self.browser.find_element_by_id("history_price_inputBox").send_keys('4500')
        self.browser.find_element_by_id("add_history_button").click()
        
        # 다시 메인 화면으로 돌아가지고, 현재 사용금액등이 변경되어 있다.   (사용금액 6000원,    사용가능금액 294000)
        # (계속 입력은 아직 추가 x)
       
        time.sleep(1)
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('현재 사용금액 6000원', rows_text)
        self.assertIn('남은 금액 294000원', rows_text )

        rows_text =  self.find_rows_from_table_id('detail_box')
        self.assertIn('군것질 98500원', rows_text)
        self.assertIn('세끼 95500원', rows_text)
        self.assertIn('선물 100000원', rows_text)


    def find_rows_from_table_id(self, id):
        """id에서 tr을 뽑아낸 후 각 row에서 text를 뽑아내 리스트로 만들어 리턴한다."""
        table = self.browser.find_element_by_id(id)
        rows = table.find_elements_by_tag_name('tr')
        return [row.text for row in rows]