from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Student)
class StudentModelAdmin(admin.ModelAdmin):
	list_display = ['user', 'level', 'section']
	list_filter = ['user', 'level', 'section']
	search_fields = ['user', 'level', 'section']


@admin.register(models.Faculty)
class FacultyModelAdmin(admin.ModelAdmin):
	list_display = ['user', 'level', 'section']
	list_filter = ['user', 'level', 'section']
	search_fields = ['user', 'level', 'section']


@admin.register(models.Staff)
class StaffModelAdmin(admin.ModelAdmin):
	list_display = ['user', 'position']
	list_filter = ['user', 'position']
	search_fields = ['user', 'position']


@admin.register(models.Address)
class AddressModelAdmin(admin.ModelAdmin):
	list_display = ['brgy', 'town', 'province']
	list_filter = ['brgy', 'town', 'province']
	search_fields = ['brgy', 'town', 'province']


@admin.register(models.Level)
class LevelModelAdmin(admin.ModelAdmin):
	list_display = ['level', ]
	search_fields = ['level', ]


@admin.register(models.Section)
class SectionModelAdmin(admin.ModelAdmin):
	list_display = ['section', 'level', ]
	search_fields = ['section', 'level', ]