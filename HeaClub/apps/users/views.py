# -*- coding:utf-8 -*-

from django.views.decorators.csrf import csrf_exempt

import json

from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from HeaClub import settings
from course.models import Course
from teachers.models import Teacher
from users.forms import LoginForm, RegisterForm, UploadImageForm
from users.models import UserMessage, UserFavorite, UserSign, UserMember
from utils.pay import AliPay


class IndexView(View):
    def get(self,request):
        all_course=Course.objects.all()[0:4]
        all_teacher=Teacher.objects.all()[0:4]
        return render(request, "index.html", {"all_course":all_course,"all_teacher":all_teacher})


class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            all_course = Course.objects.all()[0:5]
            all_teacher = Teacher.objects.all()[0:5]
            # django用户认证方法
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.type=='tea':
                    return render(request, "teacher-info.html")
                else:
                    return render(request, "index.html",{"all_course":all_course,"all_teacher":all_teacher})
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})

#---用户注册----
class  RegisterView(View):

    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            class_id=request.POST.get("class_id","class_id")
            if UserMessage.objects.filter(username=username):
                return render(request,'register.html',{'register_form':register_form,'msg':u"用户已存在"})
            user_obj=UserMessage()
            user_obj.username=username
            user_obj.type=class_id
            #密码需要加密
           # make_password加密
            user_obj.password=  make_password(password)
            user_obj.save()
            #如果教练加到Teacher表
            if class_id=='tea':
                tea_obj=Teacher(user=user_obj)
                tea_obj.save()
            return render(request,'login.html',{'register_form':register_form})
        return render(request, 'register.html', {'register_form': register_form})

class LogoutView(View):
    """
    用户登出
    pass
    # """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class UserinfoView(View):

    """
    # 用户个人信息
    # """
    def get(self, request):

        if request.user.type == 'tea':
            tea_obj=Teacher.objects.get(user=request.user)
            return render(request, "teacher-info.html",{"tea_obj":tea_obj})
        else:
            return render(request, 'usercenter-info.html', {})

    def post(self, request):
        data=(QueryDict(request.POST.get("data")))
        username=data['username']
        birthday=data["birthday"]
        sex=data["sex"]
        address=data["address"]
        mobile=data["mobile"]
        detail=data["detail"]
        user_info_obj=UserMessage.objects.get(id=request.user.id)
        user_info_obj.username=username
        if birthday:
            user_info_obj.birthday = birthday
        user_info_obj.sex = sex
        user_info_obj.address = address
        user_info_obj.mobile = mobile
        #简介添加到教练列表

        tea_obj=Teacher.objects.get(user=request.user)
        tea_obj.detail=detail
        try:
            user_info_obj.save()
            tea_obj.save()
        except Exception as  e:
            print(e)
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        return HttpResponse('{"status":"success"}', content_type='application/json')







class UploadImageView(View):

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class MemberView(View):
    def get(self,request):
        return render(request, 'user-mem.html', {})

    def post(self,request):

        order_no= '%s%d' % (datetime.now().strftime('%Y%m%d%H%M%S'), request.user.id)
        #创建订单
        user_m=UserMember(user=request.user,price=298,mem_time=datetime.now(),order_no=order_no)
        user_m.save()
        alipay = Get_AliPay_Object()
        #生成订单号
        out_trade_no="hy"+ str(datetime.now())
        #生成支付
        query_params = alipay.direct_pay(
            subject='开通会员',
            out_trade_no=order_no,  #订单号
            total_amount=str('298.00'),  # 交易金额
        )

        # 支付宝网关地址（沙箱应用）
        pay_url = settings.ALIPAY_URL + "?{0}".format(query_params)
        # return HttpResponseRedirect(pay_url)
        # 页面重定向到支付页面
        return JsonResponse({"res": 3, "pay_url": pay_url})

class SignView(View):

    def get(self,request):
        now_time = datetime.now()
        all_sign=UserSign.objects.filter(user=request.user,signdate__month=now_time.month)
        all_day= [_day.day for _day in all_sign]
        all_day=json.dumps(all_day)
        today = datetime.now().date()
        us_count = UserSign.objects.filter(user=request.user, signdate=today).count()
        return render(request, 'sign.html',{"all_sign":all_sign,"all_day":all_day,"us_count":us_count})

    def post(self,request):
        today = datetime.now().date()
        us_obj=UserSign.objects.filter(user=request.user,signdate=today)
        if us_obj.count()==0:
            us_obj=UserSign(user=request.user,signdate=datetime.today(),day=today.day)
            us_obj.save()
        return HttpResponse('{"status":"ok"}', content_type='application/json')




class MyFavTeacherView(View):

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = UserMessage.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list
        })


class MyFavCourseView(View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list
        })




# from utils.pay import AliPay

# AliPay 对象实例化
def Get_AliPay_Object():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,  # APPID （沙箱应用）
        app_notify_url="http://127.0.0.1:8000/users/pay_result",  # 回调通知地址
        return_url="http://127.0.0.1:8000/users/pay_result",  # 支付完成后的跳转地址
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH,  # 应用私钥
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
        debug=True,  # 默认False,
    )
    return alipay

    # 发起支付请求





class PayResultView(View):
    def get(self,request):
        alipay = Get_AliPay_Object()
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)

        out_trade_no=params.pop('out_trade_no')
        trade_no=params.pop('trade_no')#支付宝订单号
        user_m=UserMember.objects.get(order_no=out_trade_no)
        user_m.sale_no=trade_no
        pay_status='1'

        um_obj=UserMessage.objects.get(id=request.user.id)
        um_obj.is_member=True
        um_obj.open_date=datetime.now().date()
        um_obj.save()
        return render(request, 'usercenter-info.html', {})





