# Generated by Django 2.0.4 on 2018-05-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20180529_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='halbu_week',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
