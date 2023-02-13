from django.db import models

from django.db import models
from django.conf import settings

class Check_list(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.IntegerField()
    content = models.TextField()
    place = models.CharField(max_length=30)
    stuff_list = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    

class Stuff(models.Model):
    stuff_name = models.CharField(max_length=10)
    check_id = models.ForeignKey(Check_list, on_delete=models.CASCADE)

class recommend(models.Model):
    place = models.CharField(max_length=30)
    plus_stuff = models.CharField(max_length=30)