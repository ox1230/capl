from django import forms
from main.models import History, Category

class HistoryForm(forms.models.ModelForm):
    class Meta:
        model = History
        fields = ('category', 'name', 'price',)

        widgets = {
            'category': forms.fields.Select(
                attrs = {
                     'id' : "history_category_inputBox",    
                     'class' : "form-control input-lg",
                }
            ),
            'name' : forms.fields.TextInput(
                attrs={
                    'id' : 'history_name_inputBox',
                     'class' : "form-control input-lg",
                }
            ),
            'price': forms.fields.NumberInput(
                attrs = {
                    'id' : 'history_price_inputBox',
                    'class': "form-control input-lg",

                }
            ),
        }

    def save(self):
        return super().save()