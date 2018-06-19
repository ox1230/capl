from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from main.models import Category
from .base import FunctionalTest
from unittest import skip
import time


class VisitorTest(FunctionalTest):
    
    def test_first_main_show_correct_info(self):
        """  """
        #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Cash Planner'를 표시
        self.assertIn('Cash Planner' ,self.browser.title) 

        #메인 화면에는 현재 사용금액 정보가 있다. 현재 사용 금액은 0원이다.   -- 사용가능 금액은 300000이다.
       
        rows_text = self.find_rows_from_table_id("present_box")
        self.assertIn('사용한 돈 0원', rows_text)
        self.assertIn('남은 돈 270000원', rows_text)

        # (각 category별 남은돈, 하루 할당액이 표시된다.
        rows_text =  self.find_rows_from_table_id('detail_box')

        self.assertIn('군것질 30000원 30000원 {}원'.format(30000// (7-self.weekday)), rows_text)
        self.assertIn('세끼 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
        self.assertIn('기타 100000원 100000원 {}원'.format(100000// (7-self.weekday)), rows_text)
    @skip
    def test_layout_and_styling(self):
        """layout전체가 아니라 css가 제대로 붙어졌는지 정도를 체크함"""
        #에디스는 일반 컴퓨터로 메인페이지를 방문한다
        self.browser.get(self.live_server_url)
        self.browser.set_window_size( 1024,768 )

        #에디스는 현재상황 표시 메인 상자가 가운데 위치한것을 확인한다.
        present_box = self.browser.find_elements_by_class_name('row')[0]

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


class VisualizeTest(FunctionalTest):
    def test_main_show_graph(self):
        """main 페이지에서 그래프가 잘 보이는지 확인"""
         #edith가 해당 웹사이트 방문
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Cash Planner'를 표시
        self.assertIn('Cash Planner' ,self.browser.title) 

        bars = self.browser.find_elements_by_css_selector("rect")
        #아직 그래프는 만들어지지 않았다.
        self.assertEqual(len(bars), 0)

        # 화살표 버튼을 누른다.
        self.browser.find_element_by_id("graph-down-button").click()

        time.sleep(0.5)

        bars = self.browser.find_elements_by_css_selector("rect")
        #그래프가 만들어진다.
        self.assertNotEqual(len(bars), 0)

    def test_add_history_graph_pop_up(self):
        """add_history는 나만의 할부 적용에 따른 미래의 남은 돈 상황을 보여준다.
            분류, 금액, 나만의 할부가 입력되면 저절로 그래프가 열리면서 상황을 나타낸다."""
        #에디스는 사이트에 접속한다.
        self.browser.get(self.live_server_url)

        #에디스는 add_history page로 이동한다.
        self.go_to_page("add_history")

        #아직 그래프는 없다.
        graphes = self.browser.find_element_by_css_selector("#graph")
        self.assertEqual(graphes.get_attribute("class"), "collapse")
        
        #에디스는 기타, d3.js , 24000원, 할부 2주를 입력하려 한다.
        #먼저 할부를 입력한다. 
        self.browser.find_element_by_id("history_halbu_week_inputBox").send_keys(2)

        #그래프는 반응하지 않는다. 
        time.sleep(0.3)
        self.assertEqual(graphes.get_attribute("class"), "collapse")

        #일단 할부를 지운다.
        self.browser.find_element_by_id("history_halbu_week_inputBox").clear()

        #기타, 24000원을 입력한다. 
        self.browser.find_element_by_id("history_category_inputBox").send_keys("기타")
        self.browser.find_element_by_id("history_name_inputBox").send_keys("d3js")
        self.browser.find_element_by_id("history_price_inputBox").send_keys(24000)
        #그래프는 반응하지 않는다.
        # time.sleep(0.3) 
        self.assertEqual(graphes.get_attribute("class"), "collapse")

        #다시 할부를 입력한다. 
        self.browser.find_element_by_id("history_halbu_week_inputBox").send_keys(2)
        #그래프가 반응한다.
        time.sleep(0.3)
        self.assertNotEqual(graphes.get_attribute("class"), "collapse")


