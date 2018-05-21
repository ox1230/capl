from django import forms
from .models import History, Category

class HistoryForm(forms.models.ModelForm):
    class Meta:
        model = History
        fields = ('category', 'name', 'price',)
        labels = {'category': '분류', 'name':"내용", "price": '금액'}
        widgets = {
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