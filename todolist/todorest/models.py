from django.db import models
from django.db.models.fields import CharField
import datetime

class List(models.Model):
    title = models.CharField(max_length=200, null=True,blank=True)
    task = models.CharField(max_length=200, null=True,blank=True)

class Task(models.Model):
    title = models.CharField(max_length=200, null=True,blank=True)
    deadline = models.DateTimeField(default=datetime.date.today)
    description = models.CharField(max_length=200)

