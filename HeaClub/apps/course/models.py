from datetime import datetime

from django.db import models

# Create your models here.
from users.models import UserMessage


class Course(models.Model):
    DEGREE_CHOICES = (
        ("jc","零基础"),
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    name = models.CharField(verbose_name="课程名",max_length=50)
    detail = models.TextField(verbose_name="课程详情")
    heat = models.IntegerField(verbose_name="热量(千卡)",default=30)
    degree = models.CharField(verbose_name='难度',choices=DEGREE_CHOICES, max_length=5)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)",default=0)
    students = models.IntegerField(verbose_name="学习人数",default=0)
    fav_nums = models.IntegerField(verbose_name=u"收藏人数",default=0)
    image = models.ImageField(verbose_name=u"封面图",upload_to="courses/%Y/%m",max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)
    is_member=models.BooleanField(verbose_name=u"是否会员",default=False)
    usermessage = models.ForeignKey(UserMessage,verbose_name=u'教练',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程',on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u"章节名",max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField("视频名",max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

class CourseList(models.Model):
    user= models.ForeignKey(UserMessage, verbose_name=u'教练', on_delete=models.CASCADE,default='')
    course = models.ForeignKey(Course,verbose_name=u'课程',on_delete=models.CASCADE)
    sta_time = models.DateTimeField(verbose_name=u"开始时间",default=datetime.now)
    end_time = models.DateTimeField(verbose_name=u"结束时间", default=datetime.now)

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = verbose_name


class Ctype(models.Model):
    name = models.CharField(verbose_name=u"名称",max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间",default=datetime.now)

    class Meta:
        verbose_name = "课程分类"
        verbose_name_plural = verbose_name