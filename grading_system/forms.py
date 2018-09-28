from django import forms
from django.contrib.auth import get_user_model
from .models import (FinalGrade, Subject, SubjectGrade)


User = get_user_model()


# for administrator use only
class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ['date_created', 'updated', 'slug']


class SubjectGradeCreateForm(forms.ModelForm):
    class Meta:
        model = SubjectGrade
        exclude = ['date_created', 'updated']
        labels = {
            'is_finalized': 'Finalized?',
        }
