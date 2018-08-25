from django.contrib import admin
from announcement import models
# Register your models here.


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created']
    list_filter = ['title', 'author', 'status', 'created']
    search_fields = ['title', 'author', 'status']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'active', 'author']
