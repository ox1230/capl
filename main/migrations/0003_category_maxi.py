# Generated by Django 2.0.4 on 2018-05-16 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_residual'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='maxi',
            field=models.PositiveIntegerField(default=None),
        ),
    ]
