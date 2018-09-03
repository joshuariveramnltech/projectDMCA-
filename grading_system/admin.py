from django.contrib import admin
from .models import Subject, Grade
# Register your models here.


@admin.register(Subject)
class AdminSubject(admin.ModelAdmin):
    list_display = ['name', 'level_and_section', 'instructor', 'subject_code']
    search_fields = ['level_and_section__level',
                     'level_and_section__section', 'instructor__email', 'subject_code']


@admin.register(Grade)
class AdminGrade(admin.ModelAdmin):
    list_display = ['student', 'subject',]
    search_fields = ['student__email', 'subject__name',
                     'subject__level_and_section__level', 'subject__level_and_section__section']
