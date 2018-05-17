from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category
from .base import FuntionalTest
import unittest
import time


class AlreadyVisitorTest(FuntionalTest):
    
    def test_normaly_add_history(self):
    
        #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        #메뉴에서 거래내역추가를 눌러 거래내역 추가로 이동한다.
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
        time.sleep(3)
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
        self.assertIn('기타 100000원', rows_text)

    def test_can_go_to_main_by_button(self):
        #에디스는 사이트를 방문해 거래내역추가로 이동한다
  
        self.browser.get(self.live_server_url)

        add_history_menu = self.browser.find_element_by_id("add_history_menu")
        add_history_menu.click()

        #에디스는 각 내역을 입력했지만, 취소하고 메인으로 돌아가고 싶다
        self.browser.find_element_by_id("history_category_inputBox").send_keys('군것질')
        self.browser.find_element_by_id("history_name_inputBox").send_keys('딸기바나나')
        self.browser.find_element_by_id("history_price_inputBox").send_keys('1500')

        self.browser.find_element_by_id("go_to_main").click()

        # 메인에는 아무것도 바뀌어있지 않다.
        time.sleep(1)
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('현재 사용금액 0원', rows_text)
        self.assertIn('남은 금액 300000원', rows_text )

        rows_text =  self.find_rows_from_table_id('detail_box')
        self.assertIn('군것질 100000원', rows_text)
        self.assertIn('세끼 100000원', rows_text)
        self.assertIn('기타 100000원', rows_text)