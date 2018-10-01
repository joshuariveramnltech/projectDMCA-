from django import forms
from .models import Statement
# Create your forms here


# for admin account only
class StatementCreateForm(forms.ModelForm):
    class Meta:
        model = Statement
        exclude = ['date_created', 'updated']


# for staff account only
class StatementAddForm(forms.ModelForm):
    class Meta:
        model = Statement
        exclude = ['date_created', 'updated', 'student']
