from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category,History
from main.process import db_reset ,WeekAndDay
import unittest
import time
from datetime import date, timedelta

class FuntionalTest(LiveServerTestCase):
    def setUp(self):
        """테스트 시작 전에 수행"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)   # 암묵적 대기 -- 1초
        
        db_reset()

        self.weekday = WeekAndDay.my_week_day()  #오늘의 요일
        self.date_of_a_week_ago = date.today() + timedelta(days = -7) #7일전의 날짜
    
    def tearDown(self):
        """테스트 후에 시행-- 테스트에 에러가 발생해도 실행된다"""
        self.browser.quit()
    
    def find_rows_from_table_id(self, id):
        """id에서 tr을 뽑아낸 후 각 row에서 text를 뽑아내 row별 리스트로 만들어 리턴한다."""
        table = self.browser.find_element_by_id(id)
        rows = table.find_elements_by_tag_name('tr')
        return [row.text for row in rows]
    