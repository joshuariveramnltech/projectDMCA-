from django import template
from announcement.models import Announcement

register = template.Library()

@register.inclusion_tag('latest_school_announcement.html')
def get_latest_school_announcements(count=5):
    latest_school_announcements = Announcement.objects.filter(send_to_all=True).order_by('-publish_date')[:count]
    return {'latest_school_announcements': latest_school_announcements}