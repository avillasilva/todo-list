# Generated by Django 3.1.7 on 2021-06-15 23:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todorest', '0004_auto_20210615_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 16, 5, 9, 10, 792421, tzinfo=utc)),
        ),
    ]
