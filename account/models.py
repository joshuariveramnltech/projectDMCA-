from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
# Create your models here.


class Level(models.Model):
	LEVEL_CHOICES = (
		('nursery', 'Nursery'), ('kinder', 'Kinder'),
		('grade1', 'Grade1'), ('grade2','Grade2'),
		('grade3', 'Grade3'), ('grade4', 'Grade4'),
		('grade5', 'Grade5'), ('grade6', 'Grade6'),
	)
	level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='nursery', unique=True)

	def __str__(self):
		return self.level


class Section(models.Model):
	level = models.OneToOneField(Level, on_delete=None)
	section = models.CharField(max_length=25)

	def __str__(self):
		return self.section


class Address(models.Model):
	brgy = models.CharField(max_length=200)
	town = models.CharField(max_length=200)
	province = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'Addresses'

	def __str__(self):
		return self.brgy + ", " + self.town + ", " + self.province


class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	account = models.ForeignKey(Group, on_delete=None, default=1)
	level = models.ForeignKey(Level, on_delete=None)
	section = models.ForeignKey(Section, on_delete=None)
	birthday = models.DateField()
	guardian = models.CharField(max_length=75)
	address = models.ForeignKey(Address, on_delete=None)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Accepted Format:+639999999999. Up to 12 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex, ], max_length=15, blank=True)  # validators should be a list

	def __str__(self):
		return self.user.username


class Faculty(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	account = models.ForeignKey(Group, on_delete=None, default=2)
	level = models.ForeignKey(Level, on_delete=None)
	section = models.ForeignKey(Section, on_delete=None)
	birthday = models.DateField()
	address = models.ForeignKey(Address, on_delete=None)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Accepted Format:+639999999999. Up to 12 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex, ], max_length=15, blank=True)  # validators should be a list

	class Meta:
		verbose_name_plural = 'Faculties'

	def __str__(self):
		return self.user.username


class Staff(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	account = models.ForeignKey(Group, on_delete=None, default=3)
	position = models.CharField(max_length=200)
	birthday = models.DateField()
	address = models.ForeignKey(Address, on_delete=None)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Accepted Format:+639999999999. Up to 12 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex, ], max_length=15, blank=True)  # validators should be a list

	def __str__(self):
		return self.user.username


