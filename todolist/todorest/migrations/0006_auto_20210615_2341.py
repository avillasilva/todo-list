# Generated by Django 3.1.7 on 2021-06-15 23:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todorest', '0005_auto_20210615_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 16, 5, 41, 54, 577024, tzinfo=utc)),
        ),
    ]