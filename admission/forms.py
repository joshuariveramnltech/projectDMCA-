from django import forms
from .models import AppointmentRequest


class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        exclude = ['date_created', 'is_active']
        labels = {
            'schedule': 'Date and Time of Appointment',
        }

    birthday = forms.DateField(
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yyyy'}
        ),
        input_formats=('%m/%d/%Y', )
    )

    schedule = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yyyy hour:min'},
            format='%m/%d/%Y %H:%M'
        ),
        input_formats=('%m/%d/%Y %H:%M', )
    )
