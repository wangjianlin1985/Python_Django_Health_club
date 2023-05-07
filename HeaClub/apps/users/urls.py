# -*- coding: utf-8 -*-
from django.urls import path

from users.views import UserinfoView, UploadImageView, MemberView, SignView, LogoutView, \
    MyFavTeacherView, MyFavCourseView, PayResultView

app_name="users"
urlpatterns = [
    path('info', UserinfoView.as_view(), name="user_info"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    path('member', MemberView.as_view(), name="member"),
    path('sign', SignView.as_view(), name="sign"),
    path('myfavtea', MyFavTeacherView.as_view(), name="myfavtea"),
    path('myfavcou', MyFavCourseView.as_view(), name="myfavcou"),
    path('pay_result', PayResultView.as_view(), name="pay_result"),

]

