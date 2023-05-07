from django.contrib import admin

# Register your models here.
from bbs.models import Board, Post, Comment


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name','add_time')
admin.site.register(Board,BoardAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','comment_num','read_num','is_essence','board')
admin.site.register(Post,PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','author')

admin.site.register(Comment,CommentAdmin)



