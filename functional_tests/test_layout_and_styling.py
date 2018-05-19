from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category
from .base import FuntionalTest
import unittest
import time


class VisitorTest(FuntionalTest):
    
    def test_first_main_show_correct_info(self):
        """  """
        #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Cash Planner'를 표시
        self.assertIn('Cash Planner' ,self.browser.title) 

        #메인 화면에는 현재 사용금액 정보가 있다. 현재 사용 금액은 0원이다.   -- 사용가능 금액은 300000이다.
       
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('사용한 돈 0원', rows_text)
        self.assertIn('남은 돈 300000원', rows_text)

        # (각 category별 남은돈, 하루 할당액이 표시된다.
        rows_text =  self.find_rows_from_table_id('detail_box')

        self.assertIn('군것질 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('세끼 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('기타 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)

    def test_layout_and_styling(self):
        """layout전체가 아니라 css가 제대로 붙어졌는지 정도를 체크함"""
        #에디스는 일반 컴퓨터로 메인페이지를 방문한다
        self.browser.get(self.live_server_url)
        self.browser.set_window_size( 1024,768 )

        #에디스는 현재상황 표시 메인 상자가 가운데 위치한것을 확인한다.
        present_box = self.browser.find_element_by_id('present_box')

        self.assertAlmostEqual(
            present_box.location['x'] + present_box.size['width']/2,
            512,
            delta = 10
        )

        #에디스는 add_history 상자도 가운데 위치한것을 확인한다.
        add_history_menu = self.browser.find_element_by_id("add_history_menu")
        add_history_menu.click()

        time.sleep(1)
        add_history_box = self.browser.find_element_by_id("normally_add_history_box")
        # print(add_history_box.location['x'], "   ", add_history_box.size['width'])
        self.assertAlmostEqual(
            add_history_box.location['x'] + add_history_box.size['width']/2,
            512,
            delta = 10
        )

