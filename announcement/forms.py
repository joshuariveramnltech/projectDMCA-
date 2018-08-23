from django import forms
from django.forms import Textarea, DateField
from .models import Announcement
# Create your forms here

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'tags', 'title',
            'body', 'publish_date',
            'send_to_group', 'status',
            'send_to_all',
            ]
        
        labels = {
            'publish_date': 'Publish Date',
            'send_to_all': 'Send to all?',
            'body': 'Content'
        }
        publish_date = forms.DateField(
            widget=forms.DateInput(
                format='%m/%d/%Y',
                attrs={'class': 'datepicker'}
                ),
            input_formats=('%m/%d/%Y', )
            )
