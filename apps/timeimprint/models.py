import uuid
import datetime

from django.db import models


# Create your models here.
class DateEvent(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name="事件Id")
    event_content = models.TextField(verbose_name='事件内容')
    date = models.DateField(null=True, default=datetime.date.today, verbose_name='日期')
    start_date = models.DateField(null=True, default=datetime.date.today, verbose_name='开始日期')
    end_date = models.DateField(null=True, default=datetime.date.today, verbose_name='结束日期')
    start_time = models.TimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.TimeField(null=True, blank=True, verbose_name='结束时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
