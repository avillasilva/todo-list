from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200, null=True, blank=True)
    tasklist = models.IntegerField()

    def __str__(self):
        return self.title