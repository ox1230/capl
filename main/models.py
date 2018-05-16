from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.TextField(default='')
    residual = models.PositiveIntegerField(default = 100000)

class History(models.Model):
    category = models.ForeignKey(Category, default = None , on_delete = models.SET_DEFAULT)
    name = models.TextField(default='')
    price = models.PositiveIntegerField(default = 0)
    

    def get_absolute_url(self):
        return reverse('add_history')
    