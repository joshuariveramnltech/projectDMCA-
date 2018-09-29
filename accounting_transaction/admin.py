from django.contrib import admin
from .models import Statement
# Register your models here.


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_year', 'date_created', 'updated']
    list_filter = ['student', 'school_year']
    search_fields = ['student__user__email',
                     'student__learner_reference_number']
