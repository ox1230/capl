
from main.models import Category, History
from django.utils import timezone
from datetime import date, timedelta


class Processing():
    """ 계산 작업이 들어간 작업을 처리한다"""

    @classmethod
    def get_total_assigned(cls):
        categories = Category.objects.exclude(assigned = None)
        
        ret = sum([cate.assigned for cate in categories])

        if ret == None:
            ret = 0

        return ret
    

    @classmethod
    def get_total_sum(cls, today= date.today()):
        weekday = today.weekday()
        # 일요일: 0, 토요일: 6
        if weekday == 6:
            weekday = 0
        else:
            weekday += 1
        week_start_date = today + timedelta(days = -weekday)
        week_end_date = week_start_date + timedelta(days = 6)

        assigned = Processing.get_total_assigned()
        histories = History.objects.filter(written_date__range=(week_start_date, week_end_date))

        ret = sum([ hist.price for hist in histories])

        if ret == None:
            ret = 0
        return ret
        
    @classmethod
    def get_total_residual(cls, today=date.today() ):
        return Processing.get_total_assigned() - Processing.get_total_sum(today)        
        
    @classmethod
    def get_category_residual(cls, cate:Category, today = date.today()):
        weekday = today.weekday()
        # 일요일: 0, 토요일: 6
        if weekday == 6:
            weekday = 0
        else:
            weekday += 1

        week_start_date = today + timedelta(days = -weekday)
        week_end_date = week_start_date + timedelta(days = 6)

        hists_of_cate = History.objects.filter(category = cate, written_date__range = (week_start_date , week_end_date) )

        total = sum([hist.price for hist in hists_of_cate])

        return cate.assigned - total

        