from django.contrib import admin
from .models import Announcement
# Register your models here.


@admin.register(Announcement)
class AdminAnnouncement(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status', )
    list_filter = ('status', 'created', 'publish', 'author', )
    search_fields = ('title', 'tags')
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
