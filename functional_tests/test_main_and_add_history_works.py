from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category
from .base import FunctionalTest

from main.views import NORMAL_DATE_FORMAT, WITHOUT_WEEKDAY_DATE_FORMAT
from datetime import date , timedelta
from unittest import skip
import time


class AlreadyVisitorTest(FunctionalTest):
        
    def test_add_history_and_can_write_history_of_past(self):
        """ 과거 내역도 저장하기"""

        #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        #메뉴에서 거래내역추가를 눌러 거래내역 추가로 이동한다.
        # edith는 오늘의 식사/군것질 거래내역,  키위바나나 , 2000원을 입력한다. 
        self.add_new_history( cate="군것질", name = "딸기바나나", price = 2000, day = date.today())
        #이어서 저번주의 세끼, 맘스터치 , 5600원을 입력한다.
        self.add_new_history( cate= "세끼", name="맘스터치", price = 5600, day =date.today() + timedelta(days= -7) )
        # 다시 메인 화면으로 돌아가지고, 현재 사용금액등이 변경되어 있다.   (사용금액 2000원,    사용가능금액 298000)
        # (계속 입력은 아직 추가 x)
       
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('사용한 돈 2000원', rows_text)
        self.assertIn('남은 돈 268000원', rows_text )

        rows_text =  self.find_rows_from_table_id('detail_box')
        self.assertIn('군것질 30000원 28000원 {}원'.format(30000// (7-self.weekday) - 2000), rows_text)
        self.assertIn('세끼 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('기타 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)


    def test_can_go_to_main_by_button(self):
        #에디스는 사이트를 방문해 거래내역추가로 이동한다
  
        self.browser.get(self.live_server_url)

        self.go_to_page("add_history")

        #에디스는 각 내역을 입력했지만, 취소하고 메인으로 돌아가고 싶다
        self.browser.find_element_by_id("history_category_inputBox").send_keys('군것질')
        self.browser.find_element_by_id("history_name_inputBox").send_keys('딸기바나나')
        self.browser.find_element_by_id("history_price_inputBox").send_keys('1500')

        self.browser.find_element_by_id("go_to_main").click()

        # 메인에는 아무것도 바뀌어있지 않다.
        time.sleep(1)
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('사용한 돈 0원', rows_text)
        self.assertIn('남은 돈 270000원', rows_text )

        rows_text =  self.find_rows_from_table_id('detail_box')
        self.assertIn('군것질 30000원 30000원 {}원'.format(30000// (7-self.weekday)), rows_text)
        self.assertIn('세끼 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('기타 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
    
class HalbuTest(FunctionalTest):
    def test_add_history_and_halbu_works(self):
        #Edith는 사이트에 접속한다. 
        self.browser.get(self.live_server_url)

        #에디스는 하리보, 10000원, 나만의 할부 5주를 입력한다. 
        self.add_new_history(cate="군것질",name= "하리보", price = 10000, halbu = 5)
        #5주이므로 2000원어치만 표시되어 있다.
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('사용한 돈 2000원', rows_text)
        self.assertIn('남은 돈 268000원', rows_text )

        rows_text =  self.find_rows_from_table_id('detail_box')
        self.assertIn('군것질 30000원 28000원 {}원'.format(30000 // (7-self.weekday) - 2000), rows_text)
        self.assertIn('세끼 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('기타 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)


        #에디스는 저번주에 구입한 맥심 모카골드 12000원 짜리를 12주 할부 처리한다.
        self.add_new_history(cate ="기타", name = "맥심 모카골드", price = 12000, halbu = 12, day = date.today() + timedelta(days= -7))

        #메인메뉴에는 1000원짜리로 기록되어 있다.
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('사용한 돈 3000원', rows_text)
        self.assertIn('남은 돈 267000원', rows_text )

        rows_text =  self.find_rows_from_table_id('detail_box')
        self.assertIn('군것질 30000원 28000원 {}원'.format(30000// (7-self.weekday) - 2000), rows_text)
        self.assertIn('세끼 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('기타 100000원 99000원 {}원'.format(99000// (7-self.weekday)) , rows_text)
