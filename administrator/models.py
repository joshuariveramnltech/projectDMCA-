from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class StudentInfo(models.Model):
    LEVEL_CHOICES = (
        ('nursery', 'Nursery'), ('kinder', 'Kinder'),
        ('grade_1','Grade_1'), ('grade_2','Grade_2'),
        ('grade_3','Grade_3'), ('grade_4','Grade_4'),
        ('grade_5','Grade_5'), ('grade_6','Grade_6'),
        )
    SECTION_CHOICES = (
        ('am', 'AM'),
        ('pm', 'PM'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.CharField(max_length=200, choices=LEVEL_CHOICES, blank=True, null=True)
    section = models.CharField(max_length=200, choices=LEVEL_CHOICES, blank=True, null=True)
    guardian = models.CharField(max_length=200)
    