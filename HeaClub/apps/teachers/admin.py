from django.contrib import admin

# Register your models here.
from teachers.models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user","fav_nums","detail")
admin.site.register(Teacher,TeacherAdmin)

