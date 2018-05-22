from django import forms
from .models import History, Category
from datetime import date

class HistoryForm(forms.models.ModelForm):
    class Meta:
        model = History
        fields = ('written_date', 'category', 'name', 'price',)
        labels = {'written_date':'일자', 'category': '분류', 'name':"내용", "price": '금액'}
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
                     'class' : "form-control input",
                }
            ),
            'name' : forms.fields.TextInput(
                attrs={
                    'id' : 'history_name_inputBox',
                     'class' : "form-control input",
                }
            ),
            'price': forms.fields.NumberInput(
                attrs = {
                    'id' : 'history_price_inputBox',
                    'class': "form-control input",
                }
            ),
        }

    def save(self):
        return super().save()