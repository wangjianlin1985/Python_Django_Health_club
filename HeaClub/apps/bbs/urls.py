# -*- coding: utf-8 -*-
from django.urls import path, re_path

from bbs.views import BIndexView, AddTieView, TieDetailView, CommentView

app_name="bbs"
urlpatterns = [
    path('', BIndexView.as_view(), name="index"),
    path('add_topic', AddTieView.as_view(), name="add_topic"),
    re_path('detail/(?P<topic_id>\d+)/', TieDetailView.as_view(), name="detail"),
    path('comment', CommentView.as_view(), name="comment"),
    ]

