from django.db import models
from django.contrib.auth import get_user_model
from account.models import LevelAndSection, Level
from datetime import datetime
from django.utils.text import slugify
from account.models import FacultyProfile, StudentProfile
from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver
from random import shuffle
# Create your models here.

User = get_user_model()

CODED_VERSION = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '0', ' ', 'a', 'b',
    'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6',
    '7', '8', '9', '0'
]


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    level_and_section = models.ForeignKey(
        LevelAndSection, on_delete=models.SET_NULL, null=True, blank=True)
    designated_instructor = models.ForeignKey(
        FacultyProfile, related_name="assigned_subject", on_delete=models.SET_NULL, null=True, blank=True)
    schedule = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    slug = models.SlugField(
        max_length=250, null=True, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-date_created', ]
        unique_together = ('subject_name', 'level_and_section')

    def __str__(self):
        if self.level_and_section:
            return "{}, {}-{}".format(
                self.subject_name,
                self.level_and_section.level,
                self.level_and_section.section
            )
        return self.subject_name


class SubjectGrade(models.Model):
    SY = []
    for year in range(2010, datetime.now().year + 15):
        SY.append((str(year) + "-" + str(year+1),
                   str(year) + "-" + str(year+1)))
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name='grade')
    school_year = models.CharField(
        max_length=25, choices=SY, default=str(datetime.now().year) + "-" + str(datetime.now().year+1))
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='subject_grade')
    instructor = models.ForeignKey(
        FacultyProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='given_grade')
    first_quarter = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    second_quarter = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    third_quarter = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    fourth_quarter = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    final_subject_grade = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    is_finalized = models.BooleanField(
        default=False, help_text="Once finalized, you can no longer make any more changes..")
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return "Subject: {} Student: {}".format(
            self.subject.subject_name,
            self.student.user.get_full_name
        )


class FinalGrade(models.Model):
    SY = []
    for year in range(2010, datetime.now().year + 15):
        SY.append((str(year) + "-" + str(year+1),
                   str(year) + "-" + str(year+1)))
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name='gwa')
    level = models.ForeignKey(
        Level, on_delete=models.SET_NULL, related_name='subject', null=True, blank=True)
    school_year = models.CharField(max_length=25, choices=SY, default=str(
        datetime.now().year) + "-" + str(datetime.now().year+1))
    gwa = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    comment = models.TextField()
    is_finalized = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = ('student', 'level')

    def __str__(self):
        return "{} GWA:{} SY: {}".format(self.student.get_full_name, self.gwa, self.school_year)


@receiver(post_save, sender=Subject)
def create_dynamic_subject_slug(sender, **kwargs):
    if kwargs['created']:
        kwargs['instance'].slug = slugify(
            kwargs['instance'].subject_name + " " + str(kwargs['instance'].id))
        kwargs['instance'].save()
