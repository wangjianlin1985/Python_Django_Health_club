from django.contrib import admin

# Register your models here.
from course.models import Course, Lesson, Video, CourseList, Ctype


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','heat','degree','learn_times','is_member','usermessage')
admin.site.register(Course,CourseAdmin)


# class LessonAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Lesson,LessonAdmin)
#
#
# class VideoAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Video,VideoAdmin)

class CourseListAdmin(admin.ModelAdmin):
    list_display =('course','sta_time','end_time')
admin.site.register(CourseList,CourseListAdmin)

class CtypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Ctype,CtypeAdmin)
