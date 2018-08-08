from django import forms
from django.contrib.auth.models import User
from datetime import datetime


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', ]

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Password don\'t match!')
        return cleaned_data['password2']        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
