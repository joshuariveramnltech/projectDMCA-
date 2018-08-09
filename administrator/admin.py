from django.contrib import admin
from .models import StudentInfo
# Register your models here.


@admin.register(StudentInfo)
class CreateStudentAccount(admin.ModelAdmin):
    pass