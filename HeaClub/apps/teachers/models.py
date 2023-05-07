#-*- codding：utf-8 -*-
from django.db import models

from users.models import UserMessage


class Teacher(models.Model):

    user = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name=u"用户")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    detail=models.TextField(verbose_name=u"描述")

    class Meta:
        verbose_name = "教练"
        verbose_name_plural = verbose_name
