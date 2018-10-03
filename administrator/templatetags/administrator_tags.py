from django import template
from account.models import Level, LevelAndSection
from django.contrib.auth import get_user_model

register = template.Library()

User = get_user_model()


@register.simple_tag
def total_students_per_year(level_id):
    student_users = User.objects.filter(
        student_profile__level_and_section__level=int(level_id))
    return student_users.count()
