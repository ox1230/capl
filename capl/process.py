from main.models import Category, History

""" 계산 작업이 들어간 작업을 처리한다"""


class Processing():
    total_sum = 0
    residual = 300000


    def add_history(cate_name:str, name:str, price:int):
        Processing.total_sum += price
        Processing.residual -= price

        cate = Category.objects.get(name = cate_name)

        History.objects.create(category = cate, name = name, price = price)

        cate.residual -= price
        cate.save()



        