# -*- coding: utf-8 -*-
from django.urls import path, re_path

from course.views import CourseListView, CourseDetailView

app_name = 'course'

urlpatterns = [
    # 课程列表
    path('list/<pindex>', CourseListView.as_view(), name='course_list'),
    re_path('course_detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
]
