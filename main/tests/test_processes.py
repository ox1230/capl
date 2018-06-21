from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Category, History , HalbuHistory
from main.process import db_reset, Processing, CategoryInfo, WeekAndDay
from main.forms import HistoryForm

from datetime import date, timedelta
import re

# Create your tests here.
def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class ProcessingTest(TestCase):
    def test_DB_reset(self):
        cate =Category.objects.create(name ="1", assigned = 1000)
        hist = History.objects.create(category = cate, name="1", price = 2000, written_date = date.today())
        
        db_reset()

        all_cates =  Category.objects.all()
        all_histes =  History.objects.all()
        self.assertNotIn(cate, all_cates)
        self.assertNotIn(hist, all_histes)

        self.assertEqual(all_cates.count(), 4)
        self.assertEqual(all_histes.count(), 3)

    def test_can_process_total_assigned(self):
        Category.objects.create(name ="1", assigned = 1000)
        Category.objects.create(name ="2", assigned = 1500)
        Category.objects.create(name ="3", assigned = 1000)

        self.assertEqual(Processing.get_informations_for_main()['total_assigned'], 3500)
    
    def test_can_process_total_residual_well(self):
        cate = Category.objects.create(name ="1", assigned = 5000)
        Category.objects.create(name ="2", assigned = 5000)
        
        History.objects.create(category = cate, name="1", price = 2000, written_date = date.today())
        History.objects.create(category = cate, name="2", price = 2000, written_date = date.today()- timedelta(days=10))

        infos_main = Processing.get_informations_for_main()
        self.assertEqual(infos_main['total_assigned'], 10000)
        self.assertEqual(infos_main['total_residual'], 8000)
    
    def test_can_process_each_categories_residual_well(self):
        cate1 = Category.objects.create(name ="c1", assigned = 10000)
        cate2 = Category.objects.create(name ="c2", assigned = 10000)
        
        History.objects.create(category = cate1, name="h1", price = 6000)
        History.objects.create(category = cate1, name="h2", price = 2000, written_date = date.today()- timedelta(days=10) )
        
        self.assertEqual(CategoryInfo.get_category_residual(cate1), 4000)
        self.assertEqual(CategoryInfo.get_category_residual(cate2), 10000)

    def test_can_process_halbu_for_total_and_each_category_residual(self):
        cate1 = Category.objects.create(name ="c1", assigned = 10000)
        
        form = HistoryForm(data = {'category':cate1.id, 'price': 2400, 'written_date': date.today(), 'name': 'h1', 'halbu_week':2})
        form.save()
        
        form2 = HistoryForm(data = {'category':cate1.id, 'price': 3200, 'written_date': date.today() + timedelta(days= -7), 'name': 'h1', 'halbu_week':2})
        # 1주일 전것 추가\
        form2.save()

        cateinfo = CategoryInfo(cate1)
        self.assertEqual(cateinfo.resid, 10000- 1200 - 1600)
        self.assertEqual(cateinfo.for_day, (10000-1600)//(7-WeekAndDay.my_week_day())   - 1200)

        infos_main = Processing.get_informations_for_main()
        self.assertEqual(infos_main['total_assigned'], 10000)
        self.assertEqual(infos_main['total_sum'], 2800)
        self.assertEqual(infos_main['total_residual'], 10000- 1200 - 1600)
    
    def test_data_for_add_history_visualization(self):
        """add_history를 위한 data rendering 하기:   {category이름: [assign,[20주치 residual 데이터]]순으로  }으로 되어야 한다. """
        cate1 = Category.objects.create(name ="c1", assigned = 10000)

        #이번주 순수 금액 추가
        form = HistoryForm(data = {'category':cate1.id, 'price': 2000, 'written_date': date.today(), 'name': 'h1'})
        form.save()
        
        form2 = HistoryForm(data = {'category':cate1.id, 'price': 21000, 'written_date': date.today() + timedelta(days= -7) , 'name': 'h2', 'halbu_week':21})
        # 1주일 전것 추가\(할부 21주:   각주당 1000원)
        form2.save()

        form3 = HistoryForm(data = {'category':cate1.id, 'price': 10000, 'written_date': date.today(), 'name': 'h3', 'halbu_week':10})
        # (할부 10주:   각주당 1000원)
        form3.save()

        # show_history를 위한 데이터 얻기
        data = Processing.get_informations_for_add_history(today = date.today()) 

        json_data = data['json']

        expected_list = [6000]
        for i in range(9):
            expected_list.append(8000)
        for i in range(10):
            expected_list.append(9000)


        self.assertJSONEqual(
             json_data,
            {'c1':[10000, expected_list]}
        )




class CategoryInfoTest(TestCase):
    def test_category_info_init_well(self):
        cate1 = Category.objects.create(name ="c1", assigned = 10000)
        
        History.objects.create(category = cate1, name="h1", price = 6000)

        cate_info1 = CategoryInfo(cate1)

        self.assertEqual(cate_info1.category, cate1)
        self.assertEqual(cate_info1.name,'c1')
        self.assertEqual(cate_info1.assigned, 10000)
        self.assertEqual(cate_info1.for_day , 10000//(7- WeekAndDay.my_week_day()) -6000)   #오늘의 할당량에서 방금쓴 6000원을 뺀다.