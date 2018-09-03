from django.db import models
from django.contrib.auth import get_user_model
from account.models import LevelAndSection
# Create your models here.

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=50, null=True, blank=True)
    instructor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_subject')
    level_and_section = models.ForeignKey(
        LevelAndSection, on_delete=models.SET_NULL, related_name='subject', null=True, blank=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-date_created', ]

    def __str__(self):
        return "Subject: {}, Level and Section: {} {}, Instructor: {}".format(
            self.name,
            self.level_and_section.level,
            self.level_and_section.section,
            self.instructor.get_full_name
        )


class Grade(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='grade')
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, blank=True)
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
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return "Subject: {} Student: {}".format(self.subject.name, self.student.get_full_name)
