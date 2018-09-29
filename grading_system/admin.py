from django.contrib import admin
from .models import Subject, SubjectGrade, FinalGrade, GeneralSchoolYear
# Register your models here.


@admin.register(Subject)
class AdminSubject(admin.ModelAdmin):
    list_display = ('subject_name', 'level_and_section',
                    'designated_instructor', 'slug')
    search_fields = ('subject_name', 'designated_instructor__user__email',
                     'level_and_section__level__level', 'level_and_section__section')


@admin.register(SubjectGrade)
class AdminSubjectGrade(admin.ModelAdmin):
    list_display = ('student', 'subject', )
    search_fields = ('student__email', 'subject__subject_name',
                     'subject__level_and_section__level', 'subject__level_and_section__section')


@admin.register(FinalGrade)
class AdminFinalGrade(admin.ModelAdmin):
    list_display = ('student', 'grade', 'level', 'school_year')
    search_fields = ('student__email', 'school_year', 'level__level')


@admin.register(GeneralSchoolYear)
class GeneralSchoolYearAdmin(admin.ModelAdmin):
    list_display = ['school_year']