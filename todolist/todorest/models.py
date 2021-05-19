from django.db import models
from django.db import models
from django.contrib.auth.models import User

from datetime import date, timedelta

class TaskList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True,blank=True)

class Task(models.Model):
    ownerList = models.OneToOneField(TaskList, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True,blank=True)
    deadline = models.DateTimeField(default=date.today+timedelta(hours=6))
    description = models.CharField(max_length=200)

