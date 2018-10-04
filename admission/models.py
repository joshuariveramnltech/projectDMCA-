from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime, date
from django.utils import timezone
# Create your models here.

phone_regex = RegexValidator(
    regex=r'^\d{4}\-\d{3}\-\d{4}$', message="Accepted Format:0999-999-9999.")
age_regex = RegexValidator(
    regex=r'^\d{2}\-yrs old$', message="Accepted Format: 'age'-yrs old")

GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))


class AppointmentRequest(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    age = models.CharField(max_length=10)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=25, choices=GENDER_CHOICES,
        default='male'
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    guardian = models.CharField(max_length=50, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(
        validators=[phone_regex, ],
        max_length=15,
        blank=True, null=True,
        help_text="Please use the format: 0999-999-9999"
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Active Request?')
    schedule = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True,
                            null=True, editable=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = "Appointment Requests"
        unique_together = ('is_active', 'email')
        ordering = ('-date_created', )

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def get_complete_name(self):
        if self.middle_name:
            return self.first_name + " " + self.middle_name + " " + self.last_name
        return self.first_name + " " + self.last_name


@receiver(post_save, sender=AppointmentRequest)
def generate_appointment_slug(sender, **kwargs):
    if kwargs['created'] or kwargs['instance'].slug == None:
        kwargs['instance'].slug = slugify(str(kwargs['instance'].date_created) + " " +
                                          str(kwargs['instance'].id))
        kwargs['instance'].save()
