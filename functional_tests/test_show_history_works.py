from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category
from .base import FuntionalTest

from main.views import NORMAL_DATE_FORMAT, WITHOUT_WEEKDAY_DATE_FORMAT
from datetime import date , timedelta
import unittest
import time


class AlreadyVisitorTest(FuntionalTest):
        
    def test_show_history_show_histories_well(self):

         #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

      #에디스는 사이트에 접속해 "얼마나 썼지?"에 들어간다.
        add_history_menu = self.browser.find_element_by_id("show_history_menu")
        add_history_menu.click()

        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/show_history/')


      #"얼마나 썼지?"는 지난주의 데이터를 보여준다.  (아직 이번주의 데이터는 없다.)
        
        self.assertEqual(len(self.find_rows_from_table_id("this_week_history_box")),1)  #처음 데이터 외에는 행이 없다.

        long_ago = self.find_rows_from_table_id("long_ago_history_box")

        self.assertIn("{} 세끼 우라 2000원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
        self.assertIn("{} 세끼 학식 2700원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
        self.assertIn("{} 기타 JAVA의 정석 15500원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)

      # 바로 기록하기를 눌러 오늘/ 딸기바나나/ 군것질/ 2000원 데이터를 추가한다.
        add_history_menu = self.browser.find_element_by_id("add_history_menu")
        add_history_menu.click()

        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/add_history/')

        self.browser.find_element_by_id("history_category_inputBox").send_keys('군것질')
        self.browser.find_element_by_id("history_name_inputBox").send_keys('키위바나나')
        self.browser.find_element_by_id("history_price_inputBox").send_keys('2000')
        self.browser.find_element_by_id("add_history_button").click()

        #다시 "얼마나 썼지?"에 가보니 이번주의 데이터가 추가되어 있다.
        add_history_menu = self.browser.find_element_by_id("show_history_menu")
        add_history_menu.click()

        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/show_history/')

        self.assertIn(
            "{} 군것질 키위바나나 2000원".format(date.today().strftime(WITHOUT_WEEKDAY_DATE_FORMAT)),
            self.find_rows_from_table_id("this_week_history_box")
        )


        long_ago = self.find_rows_from_table_id("long_ago_history_box")
        
        self.assertIn("{} 세끼 우라 2000원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
        self.assertIn("{} 세끼 학식 2700원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
        self.assertIn("{} 기타 JAVA의 정석 15500원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)


