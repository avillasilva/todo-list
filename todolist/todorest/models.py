from django.db import models
from django.contrib.auth.models import User
import django

from datetime import timedelta


class TaskList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Task(models.Model):
    ownerList = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    deadline = models.DateTimeField(
        default=django.utils.timezone.now()+timedelta(hours=6))
    description = models.CharField(max_length=200)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
