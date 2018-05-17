from main.models import Category, History



class Processing():
    """ 계산 작업이 들어간 작업을 처리한다"""
    @classmethod
    def add_history(cls, cate_id:str, name:str, price:int):

        cate = Category.objects.get(id = cate_id)

        History.objects.create(category = cate, name = name, price = price)

        cate.residual -= price
        cate.save()

    @classmethod
    def get_total_assigned(cls):
        categories = Category.objects.exclude(assigned = None)
        
        ret = sum([cate.assigned for cate in categories])

        if ret == None:
            ret = 0

        return ret
    

    @classmethod
    def get_total_sum(cls):
        assigned = Processing.get_total_assigned()

        histories = History.objects.all()

        ret = sum([ hist.price for hist in histories])

        if ret == None:
            ret = 0
        return ret
        
    @classmethod
    def get_total_residual(cls):
        return Processing.get_total_assigned() - Processing.get_total_sum()        
        


        