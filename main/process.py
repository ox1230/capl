
from django.db.models.query import QuerySet
from main.models import Category, History
from django.utils import timezone
from datetime import date, timedelta

def db_reset():
    
    if History.objects.count() >0 : History.objects.all().delete()
    if Category.objects.count() >0 : Category.objects.all().delete()

    #미리 설정되어 있는 데이터
    Category.objects.create(name = '군것질', assigned = 100000)
    cate_seggi = Category.objects.create(name = '세끼', assigned = 100000)
    cate_gita = Category.objects.create(name = '기타', assigned = 100000)


    #저번주의 데이터가 이미 들어가 있다.
    History.objects.create(category= cate_seggi, price = 2000, name = "우라" ,written_date = date.today() + timedelta(days = -7)  )
    History.objects.create(category= cate_seggi, price = 2700, name = "학식" ,written_date = date.today() + timedelta(days = -7)  )
    History.objects.create(category= cate_gita, price = 15500, name = "JAVA의 정석" ,written_date = date.today() + timedelta(days = -7)  )

class CategoryInfo:
    """특히 main과 관련된 각 category의 각종 정보를 저장한다.
    @값들: category, name, assigned, resid, for_day"""
    def __init__(self, cate, resid = None, for_day= None , today = date.today()):
        self.category = cate
        self.name = cate.name
        self.assigned = cate.assigned
        self.resid = resid
        self.for_day = for_day
        
        if self.resid == None:
            self.resid = CategoryInfo.get_category_residual(cate, today)
        
        if self.for_day == None:
            weekday = today.weekday()
            # 일요일: 0, 토요일: 6
            if weekday == 6:
                weekday = 0
            else:
                weekday += 1

            self.for_day = self.resid // (7-weekday)
        
    def __str__(self):
        return "category:{}, resid:{}, for_day:{}".format(self.category.name,self.resid,self.for_day)

    @classmethod
    def get_category_sum(cls, cate:Category, today = date.today()):
        
        
        hists_of_cate = History.objects.filter(category = cate,
            written_date__range = WeekAndDay.get_week_start_and_end_date(today) )

        ret = sum([hist.price for hist in hists_of_cate])
        if ret == None:
            ret = 0
        
        return ret

    @classmethod
    def get_category_residual(cls, cate:Category , today = date.today()):
    
        return cate.assigned - CategoryInfo.get_category_sum(cate, today)

###### End Of CategoryInfo #####################

class WeekAndDay:
    """각종 날짜 관련 작업들"""
    @classmethod
    def my_week_day(cls, today = date.today()):
        """요일 리턴
        @ sun:0 ~ sat: 6"""
        
        weekday = today.weekday()
      
        if weekday == 6:
            weekday = 0
        else:
            weekday += 1
        
        return weekday
    
    @classmethod
    def get_week_start_and_end_date(cls, today = date.today()):
        """ret:  tuple(start date(sunday) of "today"'s week ,  end date(saturday) of "today"'s week)"""
        weekday = WeekAndDay.my_week_day(today)
        week_start_date = today + timedelta(days = -weekday)
        week_end_date = week_start_date + timedelta(days = 6)

        return (week_start_date, week_end_date)




###### End of WeekAndDay #####################################
class Processing():
    """중복된 작업에 대한 최적화 작업"""
    @classmethod
    def get_informations_for_main(cls, today = date.today()):
        """main,  view의 home_page를 위한 정보를 얻는 최적화된 함수
        @return: total_assigned, total_sum , list_of_category_info"""
        ret = {}
        ret['list_of_category_info'] = []
        categories = Category.objects.exclude(assigned = None)
        
        # total_assigned 계산 포함시키기
        # total_sum 계산 category_residual포함
        total_assigned = 0
        total_sum = 0
        for cate in categories:
            cate_info = CategoryInfo(cate)
            ret['list_of_category_info'].append(cate_info)
            
            total_assigned += cate.assigned
            total_sum += cate.assigned - cate_info.resid
        
        ret["total_assigned"] = total_assigned
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
    #         ret += CategoryInfo.get_category_sum(cate, today)

    #     if ret == None:
    #         ret = 0
    #     return ret
        
    # @classmethod
    # def get_total_residual(cls, today=date.today() ):
    #     return Processing.get_total_assigned() - Processing.get_total_sum(today)        
        


        