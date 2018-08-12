from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.StudentProfile)
class StudentModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'level_and_section', )
	list_filter = ('user', 'level_and_section')
	search_fields = ('user', 'level_and_section')


@admin.register(models.FacultyProfile)
class StudentModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'level_and_section', )
	list_filter = ('user', 'level_and_section')
	search_fields = ('user', 'level_and_section')


@admin.register(models.StaffProfile)
class StudentModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'position', )


@admin.register(models.Address)
class AddressModelAdmin(admin.ModelAdmin):
	list_display = ['brgy', 'town', 'province']
	list_filter = ['brgy', 'town', 'province']
	search_fields = ['brgy', 'town', 'province']


@admin.register(models.LevelAndSection)
class LevelAndSectionModelAdmin(admin.ModelAdmin):
	list_display = ['level', 'section']
	search_fields = ['level', 'section']
