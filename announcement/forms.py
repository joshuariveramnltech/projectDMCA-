from django import forms
from django.forms import Textarea, DateField, DateTimeField
from .models import Announcement, Comment
from django.utils import timezone
from datetime import datetime
# Create your forms here


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'title',
            'body', 'file', 'publish_date',
            'send_to_group', 'status',
            'send_to_all',
        ]

        labels = {
            'publish_date': 'Publish Date',
            'send_to_all': 'Send to all?',
            'body': 'Content',
            'file': 'Attach File/s'
        }

        widgets = {
            'body': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
    publish_date = forms.DateField(
        initial=datetime.now().date(), required=False,
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={'placeholder': 'mm/dd/yyyy'}
        ),
        input_formats=('%m/%d/%Y', )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'announcement', 'active']
        labels = {
            'body': 'Comment',
        }

        widgets = {
            'body': Textarea(attrs={'rows': 1, 'cols': 60}),
        }


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'announcement', 'active']
        labels = {
            'body': '',
        }

        widgets = {
            'body': Textarea(attrs={'rows': 1, 'cols': 60}),
        }
