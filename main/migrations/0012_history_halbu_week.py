# Generated by Django 2.0.4 on 2018-05-29 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180517_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='halbu_week',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
