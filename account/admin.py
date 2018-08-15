from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, LevelAndSection
from django.contrib.auth import get_user_model
from .forms import UserAdmin


# Register your models here.
User = get_user_model()
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']

@admin.register(LevelAndSection)
class LevelSectionAdminModel(admin.ModelAdmin):
    list_display = ['level', 'section']
    list_filter = ['level', 'section']
    search_fields = ['level', 'section']