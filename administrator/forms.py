from django import forms
from django.contrib.auth import get_user_model
from admission.models import AppointmentRequest

# Create forms here

User = get_user_model()


class AppointmentRequestFormAdmin(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        exclude = ['date_created', ]
