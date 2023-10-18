from django.db import models


# Create your models here.
class DateEvent(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30, blank=True, null=True)