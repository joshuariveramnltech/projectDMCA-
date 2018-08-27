from django.contrib import admin
from django.contrib.auth.models import Group
from .models import LevelAndSection, Profile
from django.contrib.auth import get_user_model
from .forms import UserAdmin


# Register your models here.
User = get_user_model()
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level_and_section', 'position']
    search_fields = ['user__email',
                     'level_and_section__level', 'level_and_section__section']


@admin.register(LevelAndSection)
class LevelSectionAdminModel(admin.ModelAdmin):
    list_display = ['level', 'section', 'adviser']
    list_filter = ['level', 'section', 'adviser__email']
    search_fields = ['level', 'section', 'adviser__email']
