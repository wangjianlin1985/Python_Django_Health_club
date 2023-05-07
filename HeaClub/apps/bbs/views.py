#-*- coding：utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from bbs.forms import AddTieForm, CommentForm
from bbs.models import Board, Post, Comment


class BIndexView(View):
    """
    主页
    """
    def get(self, request):

        boards = Board.objects.all()
        ties = Post.objects.all().order_by("-add_time")
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在title字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            ties = ties.filter(Q(title__icontains=search_keywords) | Q(content__icontains=search_keywords))
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "essence":
                ties = ties.filter(is_essence=True)
            elif sort == "read":
                ties = ties.order_by("-read_num")
            elif sort == "comment":
                ties = ties.order_by("-comment_num")
        current_id = request.GET.get('current_id', "")
        if current_id:
            ties = ties.filter(board_id=int(current_id))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(ties, 8)
        ties = p.page(page)
        return render(request, 'bbs_index.html', {"boards": boards,
                                                    "ties": ties,
                                                    "sort": sort,
                                                    'current_id': current_id,

                                                  })


class AddTieView(LoginRequiredMixin,View):
    """
    发布帖子
    """
    def get(self, request):

        boards = Board.objects.all()
        return render(request, 'bbs_add.html', {"boards": boards})

    def post(self, request):
        add_form = AddTieForm(request.POST)
        if add_form.is_valid():
            title = request.POST.get("title", "")
            content = request.POST.get("content", "")
            board_id = request.POST.get("board_id", "")

            tie = Post(title=title, author=request.user, content=content, board_id=board_id)
            tie.save()
            return HttpResponseRedirect(reverse("bbs:index"))
        else:
            return HttpResponse('重新发送')


class TieDetailView(LoginRequiredMixin,View):
    """
    帖子详情页
    """
    def get(self, request, topic_id):
        tie = Post.objects.get(id=topic_id)
        tie.read_num += 1
        tie.save()
        comments = Comment.objects.filter(post_id=topic_id).order_by('-add_time')
        return render(request, 'tic_detail.html', {"tie": tie, "comments": comments})


class CommentView(LoginRequiredMixin,View):
    """
    评论
    """
    def post(self, request):

        add_form = CommentForm(request.POST)
        if add_form.is_valid():
            content = request.POST.get("content", "")
            tie_id = request.POST.get("tie_id", "")
            comment = Comment(author=request.user, content=content, post_id=tie_id)
            comment.save()
            tie = Post.objects.get(id=tie_id)
            tie.comment_num += 1
            tie.save()
            return HttpResponseRedirect(reverse("bbs:detail", args=(tie_id,)))
        else:
            return HttpResponse('重新评论')
