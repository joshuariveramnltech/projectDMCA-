from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (LevelAndSection, Profile, Level,
                     StudentProfile, FacultyProfile, StaffProfile)
from django.contrib.auth import get_user_model
from .forms import UserAdmin
# Register your models here.


User = get_user_model()
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]
    search_fields = ['user__email', 'user__first_name', 'user__last_name', ]


@admin.register(LevelAndSection)
class LevelSectionAdmin(admin.ModelAdmin):
    list_display = ['level', 'section', 'adviser']
    list_filter = ['level', 'section', 'adviser__user__email', ]
    search_fields = [
        'level__level', 'section',
        'adviser__user__email', 'adviser__user__first_name',
        'adviser__user__last_name', 'adviser__user__middle_name'
    ]


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level', 'slug', 'date_created', 'updated']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level_and_section')
    search_fields = ('user__email', 'level_and_section__level',
                     'level_and_section__section', 'user__first_name', 'user__last_name')
    list_filter = ('level_and_section__level', 'level_and_section__section')


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designated_year_level')
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'designated_year_level__level')


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'position')
