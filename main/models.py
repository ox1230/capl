from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.TextField(default='')
    residual = models.IntegerField(default = 100000)
    assigned = models.PositiveIntegerField(blank=True, null=True, default = None)

    def __str__(self):
        return self.name

class History(models.Model):
    category = models.ForeignKey(Category, default = None , on_delete = models.SET_DEFAULT)
    name = models.TextField(default='' , null = True , blank = True)
    price = models.PositiveIntegerField(default = 0)
    




    def get_absolute_url(self):
        return reverse('add_history')
    