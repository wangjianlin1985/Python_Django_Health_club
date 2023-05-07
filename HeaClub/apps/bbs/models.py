# -*- coding:utf-8 -*-
from datetime import datetime
from django.db import models

# Create your models here.
from users.models import UserMessage


class Board(models.Model):
    name = models.CharField(max_length=20, verbose_name='板块名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '板块'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题')
    content = models.TextField(verbose_name="帖子详情", default='')
    comment_num = models.IntegerField(default=0, verbose_name='评论数')
    read_num = models.IntegerField(default=0, verbose_name='阅读数')
    is_essence = models.BooleanField(default=False, verbose_name='加精')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='板块')
    author = models.ForeignKey(UserMessage, default='', on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name="评论详情", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='帖子')
    author = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Notify(models.Model):
    name=models.CharField(max_length=30,verbose_name=u"公告名称")
    content = models.TextField(verbose_name="公告内容", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '论坛公告'
        verbose_name_plural = verbose_name


