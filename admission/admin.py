from django.contrib import admin
from .models import AppointmentRequest
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
# Register your models here.


def request_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admission:appointment_request_pdf', args=[obj.id, obj.slug])))

request_pdf.short_description = 'Appointment Request Voucher'


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'email', 'address', 'slug', 'is_active', request_pdf]
    search_fields = ['first_name', 'last_name', 'email', 'address', 'slug']
