from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from course.models import Course
from users.models import UserFavorite


class CourseListView(View):
    def get(self,request,pindex):
        sort = request.GET.get('sort', "")
        # 查询全部课程
        all_course=Course.objects.all()
        count=all_course.count()
        if sort:
            if sort == "fav_nums":
                all_course = all_course.order_by("fav_nums")

        paginator = Paginator(all_course, 2)
        page_num = request.GET.get('page', 1)

        page_of_course = paginator.page(page_num)
        print(page_of_course.has_next())
        hot_courses = Course.objects.order_by('fav_nums')[0:2]
        return render(request,'course-list.html',{"all_course":page_of_course,"hot_courses":hot_courses,"count":count})


class CourseDetailView(View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))


        #是否收藏课程
        has_fav_course = False
        if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=int(course_id)):
            has_course_faved = True
        # if request.user.is_authenticated():
        #     if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
        #         has_fav_course = True
        #
        #     if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
        #         has_fav_org = True
        #
        # tag = course.tag
        # if tag:
        #     relate_coures = Course.objects.filter(tag=tag)[:1]
        # else:
        #     relate_coures = []
        return render(request, "course-detail.html", {
            "course":course,
            # "relate_coures":relate_coures,
            "has_fav_course":has_fav_course,
            # "has_fav_org":has_fav_org
        })