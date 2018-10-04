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
            attrs={'class': 'datepicker', }), )

    schedule = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'datepicker', })
    )

    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'class': '', 'placeholder': 'hour:min:sec'})
    )
