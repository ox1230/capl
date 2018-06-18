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
  

class ClassroomTest(FunctionalTest):
      
  def test_week_start_and_end_date_are_displayed(self):
            
    #edith가 Cash Planner 방문
    self.browser.get(self.live_server_url)

    # 얼마나 썼지?로 이동한다.
    self.go_to_page("show_history")
    
  
    # 날짜 구역을 확인한다.
    week_dates = self.browser.find_element_by_id("week_start_and_end_date")

    #날짜구역의 날짜가 제대로 되어 있는지 확인한다.
    text = self.week_start_date.strftime(NORMAL_DATE_FORMAT) + " ~ " + self.week_end_date.strftime(NORMAL_DATE_FORMAT)
    #text는 시작 날짜 ~ 끝 날짜 형식의 str으로 되어있다.  (예: "2018-06-10 Sunday ~ 2018-06-16 Saturday")
    self.assertEqual(week_dates.text, text)


  