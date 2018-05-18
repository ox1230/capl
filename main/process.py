
from django.db.models.query import QuerySet
from main.models import Category, History
from django.utils import timezone
from datetime import date, timedelta


def db_reset():
    
    if History.objects.count() >0 : History.objects.all().delete()
    if Category.objects.count() >0 : Category.objects.all().delete()

    #미리 설정되어 있는 데이터
    Category.objects.create(name = '군것질', assigned = 100000)
    Category.objects.create(name = '세끼', assigned = 100000)
    cate_gita = Category.objects.create(name = '기타', assigned = 100000)


    #저번주의 데이터가 이미 들어가 있다.
    History.objects.create(category= cate_gita, price = 2700, name = "학식" ,written_date = date.today() + timedelta(days = -7)  )
    

class Processing():
    """ 계산 작업이 들어간 작업을 처리한다"""
    @classmethod
    def get_informations_for_main(cls, today = date.today(), category_assigned= True):
        ret = {}
        categories = Category.objects.exclude(assigned = None)
        
        # total_assigned 계산과 cate_assigned 포함시키기
        total_assigned = 0
        for cate in categories:
            total_assigned += cate.assigned
            if category_assigned:
                ret["{}_assigned".format(cate.name)] = cate.assigned
        
        
        ret["total_assigned"] = total_assigned

        # total_sum 계산과 category_residual포함
        total_sum = 0
        for cate in categories:
            cate_residual = Processing.get_category_residual(cate,today)
            ret[cate] = cate_residual
            total_sum += cate.assigned - cate_residual
        
        ret["total_sum"] = total_sum
        ret["total_residual"] = total_assigned - total_sum 
        return ret

    # @classmethod
    # def get_total_assigned(cls):
    #     categories = Category.objects.exclude(assigned = None)
        
    #     ret = sum([cate.assigned for cate in categories])

    #     if ret == None:
    #         ret = 0

    #     return ret
    

    # @classmethod
    # def get_total_sum(cls, today= date.today()):

    #     assigned = Processing.get_total_assigned()
    #     list_of_cate = Category.objects.exclude(assigned = None)
        
    #     ret = 0
    #     for cate in list_of_cate:
    #         ret += Processing.get_category_sum(cate, today)

    #     if ret == None:
    #         ret = 0
    #     return ret
        
    # @classmethod
    # def get_total_residual(cls, today=date.today() ):
    #     return Processing.get_total_assigned() - Processing.get_total_sum(today)        
        
    @classmethod
    def get_category_sum(cls, cate:Category, today = date.today()):
        weekday = today.weekday()
        # 일요일: 0, 토요일: 6
        if weekday == 6:
            weekday = 0
        else:
            weekday += 1

        week_start_date = today + timedelta(days = -weekday)
        week_end_date = week_start_date + timedelta(days = 6)

        hists_of_cate = History.objects.filter(category = cate, written_date__range = (week_start_date , week_end_date) )

        ret = sum([hist.price for hist in hists_of_cate])
        if ret == None:
            ret = 0
        return ret

    @classmethod
    def get_category_residual(cls, cate:Category , today = date.today()):

        return cate.assigned - Processing.get_category_sum(cate, today)

        