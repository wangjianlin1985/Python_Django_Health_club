from django.contrib import admin

# Register your models here.
from .models import UserMessage, Banner, UserSign


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'birthday', 'address', 'mobile','type')

admin.site.register(UserMessage,UserMessageAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title','image','url','index')
admin.site.register(Banner,BannerAdmin)

class UserSignAdmin(admin.ModelAdmin):
    list_display = ('user','signdate')
admin.site.register(UserSign,UserSignAdmin)
