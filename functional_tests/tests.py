from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest
import time


class VisitorTest(LiveServerTestCase):
    def setUp(self):
        """테스트 시작 전에 수행"""
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)   # 암묵적 대기 -- 3초
    
    def tearDown(self):
        """테스트 후에 시행-- 테스트에 에러가 발생해도 실행된다"""
        self.browser.quit()
    
    def test_show_main_and_add_item(self):
        """  """
        #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Cash Planner'를 표시
        self.assertIn('Cash Planner' ,self.browser.title) 

        #메인 화면에는 현재 사용금액 정보가 있다. 현재 사용 금액은 0원이다.   -- 사용가능 금액은 300000이다.
        present_box = self.browser.find_element_by_id("present_box")

        rows = present_box.find_elements_by_tag_name('tr')
        self.assertIn('현재 사용금액 0원', [row.text for row in rows])
        self.assertIn('남은 금액 300000원', [row.text for row in rows])

        # (각 항목별 사용가능금액이 표시된다.)  -- 이부분 나중에 


        #메뉴에서 항목추가를 눌러 항목 추가로 이동한다.   -- 일단 하이퍼링크로 대체
        add_item_menu = self.browser.find_element_by_id("add_item_menu")
        element.click()

        time.sleep(3)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/add_item/')


        # edith는 식사/군것질 항목,  딸기 바나나, 1500원을 입력한다. 





        # 다시 메인 화면으로 돌아가고, 현재 사용금액등이 변경되어 있다.   (사용금액 1500원,    사용가능금액 298500)
        

