import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from bbs.models import Post
from course.models import Course, CourseList
from teachers.models import Teacher
from users.forms import UserInfoForm
from users.models import UserMessage, UserFavorite


class TeacherinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        tea_obj = Teacher.objects.get(user=request.user)
        return render(request, 'teacher-info.html', {"tea_obj":tea_obj})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        sort=request.GET.get("sort","")
        all_teacher = Teacher.objects.all()
        count=Teacher.objects.count()
        all_teacher.order_by("-fav_nums")
        if sort=="hot":
            all_teacher=all_teacher.order_by("fav_nums")
        paginator=Paginator(all_teacher,8)
        page_num=request.GET.get('page',1)
        page_of_teacher = paginator.get_page(page_num)
        return render(request, 'teachers-list.html',
                      {"all_teacher": page_of_teacher,"count":count}, )


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        has_teacher_faved = False

        if UserFavorite.objects.filter(user_id=request.user.id, fav_type=3, fav_id=int(teacher_id)):
            has_teacher_faved = True


        teacher = Teacher.objects.get(user_id=int(teacher_id))
        all_couse=Course.objects.filter(usermessage_id=int(teacher_id))

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_courses":all_couse,
            "has_teacher_faved": has_teacher_faved,
        })


class ReleaseCourse(LoginRequiredMixin, View):
    def get(self, request):
        all_course=Course.objects.filter(usermessage=request.user)
        # return render(request, 'rel_course.html', {})
        return render(request, 'couse-teacher.html', {"all_course":all_course})

    def post(self, request):

        name = request.POST.get("name")
        detail = request.POST.get("detail")
        heat = request.POST.get("heat")
        learm_times = request.POST.get("learn_times")
        degree = request.POST.get("degree")
        image = request.FILES.get("image")
        is_m = request.POST.get("is_m")
        c_obj = Course()
        c_obj.name = name
        c_obj.detail = detail
        c_obj.heat = heat
        c_obj.learm_times = learm_times
        c_obj.degree = degree
        c_obj.image = image
        c_obj.usermessage = request.user
        if is_m == '1':
            c_obj.is_member = True
        else:
            c_obj.is_member = False
        c_obj.save()

        return HttpResponseRedirect(reverse("teacher:relcou"))


class AddCouListView(View):
    def get(self, request):
        all_course=Course.objects.filter(usermessage=request.user)
        all_coustlist=CourseList.objects.filter(user_id=request.user.id)
        return render(request, 'add_course.html', {'all_course':all_course,"all_coustlist":all_coustlist})

    def post(self, request):
        course = request.POST.get("course")
        sta_time = request.POST.get("sta_time")
        end_time = request.POST.get("end_time")
        cl_obj=CourseList(user_id=request.user.id,course_id=course,sta_time=sta_time,end_time=end_time)
        cl_obj.save()
        return HttpResponseRedirect(reverse("teacher:addclist"))

class UpCouListView(View):

    def post(self, request):
        coulist_id = request.POST.get("couid")
        course = request.POST.get("course")
        sta_time = request.POST.get("sta_time")
        end_time = request.POST.get("end_time")
        cl_obj = CourseList.objects.get(id=int(coulist_id))
        cl_obj.course_id = int(course)
        cl_obj.sta_time = sta_time
        cl_obj.end_time = end_time
        cl_obj.save()
        return HttpResponseRedirect(reverse("teacher:addclist"))
class DeCouListView(View):

    def post(self, request):
        coulist_id=request.POST.get("_id")
        if coulist_id:
            cl_obj=CourseList.objects.get(id=int(coulist_id)).delete()
        all_course = Course.objects.filter(usermessage=request.user)
        return HttpResponse('{"status":"ok"}', content_type='application/json')

class AddFavView(View):

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # if not request.user.is_authenticated():
        #     #判断用户登录状态
        #     return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.filter(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()

            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(user_id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(user_id=int(fav_id))
                    if teacher:
                        teacher.fav_nums += 1

                    else:
                        teacher=Teacher(user=request.user,fav_nums=1)
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

class SelStuView(View):
    def get(self, request):
        all_c=Course.objects.filter(usermessage=request.user)
        all_c=[_obj.id for _obj in all_c]

        fav_courses = UserFavorite.objects.filter(fav_type=1,fav_id__in=all_c)

        students = []
        for fav_course in fav_courses:
            students.append(fav_course.user)

        students = set(students)
        return render(request, 'mystu.html', {
            "students":students
        })

class MyFanView(View):

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(fav_type=3,fav_id=request.user.id)

        return render(request, 'myfan.html', {
            "teacher_list":fav_teachers
        })
class UpCourse(View):


    def post(self, request):
        couid=request.POST.get("couid")

        name = request.POST.get("name")
        detail = request.POST.get("detail")
        heat = request.POST.get("heat")
        learm_times = request.POST.get("learn_times")
        degree = request.POST.get("degree")
        image = request.FILES.get("image")
        is_m = request.POST.get("is_m")
        if couid:
            c_obj = Course.objects.get(id=couid)
            c_obj.name = name
            c_obj.detail = detail
            c_obj.heat = heat
            c_obj.learm_times = learm_times
            c_obj.degree = degree
            if image:
                c_obj.image = image
            c_obj.usermessage = request.user
            if is_m == '1':
                c_obj.is_member = True
            else:
                c_obj.is_member = False
            c_obj.save()

        return redirect(reverse('teacher:relcou'))

class CourseDe(View):


    def post(self, request):
        couid=request.POST.get("_id")


        if couid:
            c_obj = Course.objects.get(id=couid).delete()
        all_course = Course.objects.filter(usermessage=request.user)
        return redirect(reverse('teacher:relcou'))


class DeleteBbs(View):
    def get(self,request):
        post_all=Post.objects.filter(author_id=request.user.id)
        return render(request, 'deletebbs.html', {"post_all": post_all})

    def post(self,request):
        bbsid=request.POST.get("bbsid")
        if bbsid:
            post_obj = Post.objects.get(id=int(bbsid))
            post_obj.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fa", "msg":"删除失败"}', content_type='application/json')
