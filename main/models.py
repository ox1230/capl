from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import date , timedelta

class Category(models.Model):
    name = models.TextField(default='')
    assigned = models.PositiveIntegerField(blank=True, null=True, default = None)

    def __str__(self):
        return self.name

class History(models.Model):
    category = models.ForeignKey(Category, default = None , on_delete = models.SET_DEFAULT)
    name = models.TextField(default='' , null = True , blank = True)
    price = models.PositiveIntegerField(default = 0)
    written_date = models.DateField(default = timezone.now)
    halbu_week = models.PositiveIntegerField(default = 1,  null = True , blank = True)


    def get_absolute_url(self):
        return reverse('add_history')

    def __str__(self):
        return "{} {} {} {}".format(self.written_date.strftime("%Y-%m-%d"), self.category, self.name, self.price)

class HalbuHistory(models.Model):
    history = models.ForeignKey(History, default = None , on_delete = models.CASCADE)
    category = models.ForeignKey(Category, default = None , on_delete = models.SET_DEFAULT)
    second_week_date = models.DateField(default = date.today() + timedelta(days = 7))
    last_week_date = models.DateField(default = date.today() + timedelta(days = 7))
    depre = models.PositiveIntegerField(default = 0)