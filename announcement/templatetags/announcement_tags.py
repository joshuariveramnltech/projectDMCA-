from django import template
from announcement.models import Announcement

register = template.Library()


@register.inclusion_tag('latest_school_announcement.html')
def get_latest_school_announcements(count=5):
    latest_school_announcements = Announcement.objects.filter(
        send_to_all=True).order_by('-publish_date')[:count]
    return {'latest_school_announcements': latest_school_announcements}


@register.inclusion_tag('announcements_with_similar_tags.html')
def get_announcements_with_similar_tags(announcement_id):
    announcement_id = int(announcement_id)
    announcement = Announcement.objects.get(id=announcement_id)
    announcement_tags_id = announcement.tags.values_list('id', flat=True)
    similar_announcements = None
    if announcement.send_to_all:
        similar_announcements = Announcement.objects.filter(
            status='published',
            tags__in=announcement_tags_id
        ).exclude(id=announcement_id)
    elif announcement.send_to_group is not None:
        similar_announcements = Announcement.objects.filter(
            status='published',
            tags__in=announcement_tags_id,
            send_to_group=announcement.send_to_group
        ).exclude(id=announcement_id)
    return {'similar_announcements': similar_announcements}
