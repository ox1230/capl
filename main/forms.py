from django import forms
from main.models import History, Category

class HistoryForm(forms.models.ModelForm):
    class Meta:
        model = History
        fields = ('category', 'name', 'price',)

        widgets = {
            'category': forms.fields.Select(
                choices= ['첫번째','두번째'],
                attrs = {
                     'id' : "history_category_inputBox",    
                     'class' : "form-control input-lg",
                     'name' : 'history_category',
                    
                }
            ),
            'name' : forms.fields.TextInput(
                attrs={
                    'id' : 'history_name_inputBox',
                     'class' : "form-control input-lg",
                     'name' : 'history_category',
                }
            ),
            'price': forms.fields.NumberInput(
                attrs = {
                    'id' : 'history_price_inputBox',
                    'class': "form-control input-lg",
                    'name' : 'history_category',
                }
            ),
        }

 