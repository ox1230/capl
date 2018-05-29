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

    def go_to_page(self,page:str):
        add_history_menu = self.browser.find_element_by_id("{}_menu".format(page))
        add_history_menu.click()

        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/{}/'.format(page))

    def add_new_history(self, cate="군것질", name ="키위바나나", price = 2000, day = date.today(), halbu = 1):
        """새로운 history 추가 ---끝나고 메인 페이지로 이동하는것에 유의"""
        self.go_to_page( "add_history")

        self.browser.find_element_by_id("history_written_date_inputBox").clear()
        self.browser.find_element_by_id("history_written_date_inputBox").send_keys(day.strftime('%Y-%m-%d'))
        self.browser.find_element_by_id("history_category_inputBox").send_keys(cate)
        self.browser.find_element_by_id("history_name_inputBox").send_keys(name)
        self.browser.find_element_by_id("history_price_inputBox").send_keys(price)
        self.browser.find_element_by_id("history_halbu_week_inputBox").clear()
        self.browser.find_element_by_id("history_halbu_week_inputBox").send_keys(halbu)
        
        self.browser.find_element_by_id("add_history_button").click()
        time.sleep(1)
    