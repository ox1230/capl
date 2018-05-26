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
    self.go_to_page("show_history")

    #"얼마나 썼지?"는 지난주의 데이터를 보여준다.  (아직 이번주의 데이터는 없다.)      
    self.assertEqual(len(self.find_rows_from_table_id("this_week_history_box")),1)  #처음 데이터 외에는 행이 없다.

    long_ago = self.find_rows_from_table_id("long_ago_history_box")

    self.assertIn("{} 세끼 우라 2000원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
    self.assertIn("{} 세끼 학식 2700원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
    self.assertIn("{} 기타 JAVA의 정석 15500원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)

  # 바로 기록하기를 눌러 기본 데이터를 추가한다.
    self.add_new_history(cate = "군것질", name = "키위바나나", price = 2000)

    #다시 "얼마나 썼지?"에 가보니 이번주의 데이터가 추가되어 있다.
    self.go_to_page("show_history")

    self.assertIn(
        "{} 군것질 키위바나나 2000원".format(date.today().strftime(WITHOUT_WEEKDAY_DATE_FORMAT)),
        self.find_rows_from_table_id("this_week_history_box")
    )

    long_ago = self.find_rows_from_table_id("long_ago_history_box")
    
    self.assertIn("{} 세끼 우라 2000원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
    self.assertIn("{} 세끼 학식 2700원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)
    self.assertIn("{} 기타 JAVA의 정석 15500원".format(self.date_of_a_week_ago.strftime(WITHOUT_WEEKDAY_DATE_FORMAT)), long_ago)

  def test_delete_button_works_well(self):
    #edith가 해당 웹사이트 방문
    self.browser.get(self.live_server_url)

    #오늘 먹은 키위바나나에 대한 기록을 추가한다.
    self.add_new_history( cate = "군것질", name= "키위바나나", price = 2000)

    # 얼마나 썼지?에 가보니 기록이 존재한다.
    self.go_to_page("show_history")

    self.assertIn(
          "{} 군것질 키위바나나 2000원".format(date.today().strftime(WITHOUT_WEEKDAY_DATE_FORMAT)),
          self.find_rows_from_table_id("this_week_history_box")
    )

    #방금 쓴 기록을 지우고 싶어 삭제 버튼을 클릭한다. 
    self.browser.find_element_by_id(
       "{}_군것질_키위바나나_2000_delete_button".format(date.today().strftime(WITHOUT_WEEKDAY_DATE_FORMAT))).click()

    time.sleep(1)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/show_history/')

    #방금 쓴 기록은 삭제되어 존재하지 않는다.
    self.assertNotIn(
          "{} 군것질 키위바나나 2000원".format(date.today().strftime(WITHOUT_WEEKDAY_DATE_FORMAT)),
          self.find_rows_from_table_id("this_week_history_box")
    )
    
  