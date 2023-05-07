# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from teachers.views import TeacherListView, TeacherinfoView, ReleaseCourse, AddCouListView, TeacherDetailView, \
    AddFavView, SelStuView, MyFanView, UpCourse, CourseDe, UpCouListView, DeCouListView, DeleteBbs

app_name = 'teacher'
urlpatterns = [
    path('list/', TeacherListView.as_view(), name="teacher_list"),#教练列表
    path('tinfo', TeacherinfoView.as_view(), name="teacher_info"),#教练个人中心
    path('relcou', ReleaseCourse.as_view(), name="relcou"),#课程管理
    path('addclist', AddCouListView.as_view(), name="addclist"),#课程表
    path('upclist', UpCouListView.as_view(), name="upclist"),#课程表
    path('declist', DeCouListView.as_view(), name="declist"),  # 课程表
    re_path('detail/(?P<teacher_id>\d+)/',TeacherDetailView.as_view(), name="detail"),#教练详情
    path('addfav', AddFavView.as_view(), name="addfav"),#
    path('selstu', SelStuView.as_view(), name="selstu"),#查询学员
    path('myfan', MyFanView.as_view(), name="myfan"),#我的粉丝
    path('upcou', UpCourse.as_view(), name="upcou"),#课程修改
    path('coudelete', CourseDe.as_view(), name="coudelete"),#课程删除
    path('deletebbs', DeleteBbs.as_view(), name="deletebbs"),  # 删除帖子


]