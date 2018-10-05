from django import forms
from django.contrib.auth import get_user_model
from .models import (FinalGrade, Subject, SubjectGrade)


User = get_user_model()


# for administrator use only
class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ['date_created', 'updated', 'slug']


# for administrator use only
class SubjectGradeCreateForm(forms.ModelForm):
    class Meta:
        model = SubjectGrade
        exclude = [
            'date_created', 'updated',
            'student', 'instructor', 'subject'
        ]
        labels = {
            'is_finalized': 'Finalized?',
        }


# for faculty use only
class SubjectGradeEditForm(forms.ModelForm):
    class Meta:
        model = SubjectGrade
        exclude = [
            'date_created', 'updated',
            'student', 'school_year',
            'subject', 'instructor']
        labels = {
            'is_finalized': 'Finalized?',
        }


# for administrator use only
class FinalGradeCreateForm(forms.ModelForm):
    class Meta:
        model = FinalGrade
        exclude = ['student', 'date_created', 'updated', 'level']
        labels = {
            'is_finalized': 'Finalized?',
            'grade': 'Final Grade'
        }

# for faculty use only


class FinalGradeEditForm(forms.ModelForm):
    class Meta:
        model = FinalGrade
        exclude = [
            'date_created', 'updated',
            'student', 'level',
            'school_year'
        ]
        labels = {
            'is_finalized': 'Finalized?',
            'grade': 'Final Grade'
        }
