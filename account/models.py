from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
# Create your models here.


class LevelAndSection(models.Model):
	LEVEL_CHOICES = (
		('nursery', 'Nursery'), ('kinder', 'Kinder'),
		('grade1', 'Grade1'), ('grade2', 'Grade2'),
		('grade3', 'Grade3'), ('grade4', 'Grade4'),
		('grade5', 'Grade5'), ('grade6', 'Grade6'),
	)
	level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='nursery')
	section = models.CharField(max_length=25)

	def __str__(self):
		return self.level + " " + self.section


class Address(models.Model):
	brgy = models.CharField(max_length=200)
	town = models.CharField(max_length=200)
	province = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'Addresses'

	def __str__(self):
		return self.brgy + " " + self.town + ", " + self.province


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	account = models.ForeignKey(Group, on_delete=None)
	birthday = models.DateField(blank=True, null=True)
	address = models.ForeignKey(Address, on_delete=None, blank=True, null=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Accepted Format:+639999999999.")
	phone_number = models.CharField(validators=[phone_regex, ], max_length=15, blank=True, null=True)

	def __str__(self):
		return self.user.username

	class Meta:
		abstract = True


class StudentProfile(Profile):
	level_and_section = models.ForeignKey(LevelAndSection, on_delete=None, related_name='students', blank=True, null=True)
	guardian = models.CharField(max_length=200, blank=True, null=True)


class FacultyProfile(Profile):
	level_and_section = models.ForeignKey(LevelAndSection, on_delete=None, related_name='adviser', blank=True, null=True)


class StaffProfile(Profile):
	position = models.CharField(max_length=200, blank=True, null=True)
