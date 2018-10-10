from django import forms
from django.forms import Textarea
from .models import Announcement, Comment
# Create your forms here


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'title', 'tags',
            'body', 'file', 'send_to_group',
            'send_to_all',
        ]

        labels = {
            'send_to_all': 'Send to all?',
            'body': 'Content',
            'file': 'Attach File/s'
        }


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
