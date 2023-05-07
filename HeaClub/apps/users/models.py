#-*- codding:utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class UserMessage(AbstractUser):

    sex=models.CharField(max_length=6, choices=(("male",u"男"),("female","女")), default="male",verbose_name=u"性别")
    birthday=models.DateField(null=True,blank=True,verbose_name=u"生日")
    address = models.CharField(max_length=100, default=u"",verbose_name=u"地址")
    mobile = models.CharField(max_length=11, null=True, blank=True,verbose_name=u"电话号")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100,verbose_name=u"头像")
    type=models.CharField(max_length=10,choices=(("stu",u"学员"),("tea",u"教练")),verbose_name=u"用户类型")
    is_member=models.BooleanField(default=False, verbose_name='会员')
    open_date=models.DateField(null=True,blank=True,verbose_name=u"开通时间")

    class Meta:
        verbose_name=u"用户信息表"
        verbose_name_plural = verbose_name

#轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name



    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

class UserFavorite(models.Model):
    user = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name=u"用户")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    fav_type = models.IntegerField(choices=((1,"课程"),(3,"讲师")), default=1, verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name

class UserSign(models.Model):
    user = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name=u"用户")
    signdate=models.DateField(verbose_name=u"签到日期")
    day=models.CharField(max_length=3)

    class Meta:
        verbose_name = u"用户签到表"
        verbose_name_plural = verbose_name




class UserMember(models.Model):

    order_no=models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserMessage, on_delete=models.CASCADE, verbose_name=u"用户")
    sale_no = models.CharField(max_length=20,verbose_name="支付宝订单号")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="商品价格")
    mem_time=models.DateTimeField(verbose_name=u"创建时间")
    pay_status=models.CharField(max_length=6,choices=(('0',"待支付"),('1',"已支付")), default='0', verbose_name=u"支付状态")


    class Meta:
        verbose_name = u"会员开通流水表"
        verbose_name_plural = verbose_name
