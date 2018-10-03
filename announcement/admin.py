from django.contrib import admin
from announcement import models
# Register your models here.


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'date_created']
    list_filter = ['title', 'author', 'status', 'date_created']
    search_fields = ['title', 'author__email', 'status']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'active', 'author']
    search_fields = ['author__email', ]
