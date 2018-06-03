from django import forms
from main.models import History, Category, HalbuHistory
from datetime import date, timedelta
from main.process import WeekAndDay

class HistoryForm(forms.models.ModelForm):
    class Meta:
        model = History
        fields = ('written_date', 'category', 'name', 'price','halbu_week')
        labels = {'written_date':'일자', 'category': '분류', 'name':"내용", "price": '금액', 'halbu_week':'나만의 할부'}
        widgets = {
            'written_date': forms.fields.DateInput(
                attrs = {
                    'id' : 'history_written_date_inputBox',
                    'class': 'form-control input',
                    'value': date.today(),
                }
            ),
            'category': forms.fields.Select(
                attrs = {
                     'id' : "history_category_inputBox",    
                     'class' : "form-control input-xs",
                }
            ),
            'name' : forms.fields.TextInput(
                attrs={
                    'id' : 'history_name_inputBox',
                     'class' : "form-control input",
                     'autofocus':True,
                }
            ),
            'price': forms.fields.NumberInput(
                attrs = {
                    'id' : 'history_price_inputBox',
                    'class': "form-control input",
                }
            ),
            'halbu_week': forms.fields.NumberInput(
                attrs = {
                    'id' : 'history_halbu_week_inputBox',
                    'class': "form-control input",
                    'placeholder': "안씀(1주)",
                    }
            ),
        }

    def save(self):
        if self.instance.halbu_week == None or self.instance.halbu_week == 0:
           self.instance.halbu_week =1
        
        me = super().save()

        if me.halbu_week >= 2:
            HalbuHistory.objects.create(category = me.category, history = me, depre = me.price//me.halbu_week,
                second_week_date = WeekAndDay.get_week_start_and_end_date(me.written_date)[0]+ timedelta(days= 7),
                last_week_date    = WeekAndDay.get_week_start_and_end_date(me.written_date)[0]+ timedelta(days= 7*me.halbu_week - 1),
            )
        else:
            pass
        
        return me