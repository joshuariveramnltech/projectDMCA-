from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings
from datetime import date
from django.core.validators import RegexValidator
from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
# from gdstorage.storage import GoogleDriveStorage
# gd_storage = GoogleDriveStorage()
# Create your models here.

phone_regex = RegexValidator(
    regex=r'^\d{4}\-\d{3}\-\d{4}$', message="Accepted Format:0999-999-9999.")

lrn_regex = RegexValidator(regex=r'\d{12}$', message="12 digit number")

CIVIL_STATUS_CHOICES = (('single', 'Single'), ('married', 'Married'))

LEVEL_CHOICES = (
    ('Nursery', 'Nursery'), ('Kinder', 'Kinder'),
    ('Grade 1', 'Grade 1'), ('Grade 2', 'Grade 2'),
    ('Grade 3', 'Grade 3'), ('Grade 4', 'Grade 4'),
    ('Grade 5', 'Grade 5'), ('Grade 6', 'Grade 6')
)


class UserManager(BaseUserManager):
    def create_user(
        self, email=None,
        first_name=None, last_name=None,
        middle_name=None, password=None,
        is_active=True, is_staff=False,
        is_student=False, is_teacher=False,
        is_superuser=False
    ):
        if email is None:
            raise ValueError("Users must have an email address!")
        if password is None:
            raise ValueError("Users must have a password")
        if first_name is None:
            raise ValueError("Users must have a first name!")
        if last_name is None:
            raise ValueError("Users must have a last name!")
        if is_student == is_teacher == is_staff == is_superuser == False:
            raise ValueError("Users must have account type")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            middle_name=middle_name.title(),
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_student = is_student
        user.is_teacher = is_teacher
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name=first_name.title(),
            last_name=last_name.title(),
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name=first_name.title(),
            last_name=last_name.title(),
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(
        max_length=255, blank=True, null=True, help_text="Please use the format: mm/dd/yyyy")
    gender = models.CharField(
        max_length=25, blank=True, null=True, choices=GENDER_CHOICES, default='male')
    address = models.CharField(max_length=255, blank=True, default='')
    is_active = models.BooleanField(default=True, verbose_name=u"Active")
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_created', ]

    @property
    def get_full_name(self):
        if self.middle_name is not None:
            return "{} {} {}".format(
                self.first_name.title(),
                self.middle_name.title(),
                self.last_name.title()
            )
        else:
            return self.get_short_name

    @property
    def get_short_name(self):
        return "{} {}".format(self.first_name.title(), self.last_name.title())

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        self.__account_type = "Floating Account"
        if self.is_superuser:
            self.__account_type = 'Administrator'
        elif self.is_student:
            self.__account_type = 'Student'
        elif self.is_teacher:
            self.__account_type = 'Faculty/Teacher'
        elif self.is_staff:
            self.__account_type = 'Staff'
        return self.get_full_name + " (" + self.__account_type + ")"


class Level(models.Model):
    level = models.CharField(max_length=25, choices=LEVEL_CHOICES, unique=True)
    slug = models.SlugField(max_length=250, null=True,
                            blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-level', )

    def __str__(self):
        return self.level

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.level + " " + str(self.date_created)):
            self.slug = slugify(self.level + " " + str(self.date_created))
        super(Level, self).save(*args, **kwargs)


class FacultyProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='faculty_profile')
    civil_status = models.CharField(
        max_length=25, choices=CIVIL_STATUS_CHOICES, default='single')
    spouse = models.CharField(max_length=50, null=True,
                              blank=True, help_text="If Applicable", default='N/A')
    school_graduated = models.CharField(max_length=255, null=True, blank=True)
    major = models.CharField(max_length=255, null=True, blank=True)
    designated_year_level = models.ForeignKey(
        Level, related_name='year_level_teacher', on_delete=models.SET_NULL, null=True, blank=True)
    additional_information = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Faculty Profile"

    def __str__(self):
        if self.designated_year_level:
            return "{} ({})".format(self.user.get_full_name, self.designated_year_level.level)
        return "{}".format(self.user.get_full_name)


class LevelAndSection(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    section = models.CharField(max_length=50)
    adviser = models.ForeignKey(
        FacultyProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_year_and_section')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Levels and Sections'
        ordering = ('level', )
        unique_together = ('level', 'section')

    def __str__(self):
        return "{} - {}".format(self.level.level, self.section)

    def save(self, *args, **kwargs):
        if self.section is not None and self.section != self.section.upper():
            self.section = self.section.upper()
        super(LevelAndSection, self).save(*args, **kwargs)


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile")
    learner_reference_number = models.CharField(
        max_length=12, blank=True, validators=[lrn_regex, ],
        help_text="12 digit number", unique=True, default='')
    guardian = models.CharField(max_length=255, blank=True, default='')
    guardian_contact_number = models.CharField(
        validators=[phone_regex, ],
        max_length=15,
        blank=True, default='',
        help_text="Please use the format: 0999-999-9999"
    )
    level_and_section = models.ForeignKey(
        LevelAndSection, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="students"
    )
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Student Profile"

    def __str__(self):
        if self.level_and_section:
            return self.user.get_full_name + " (" + str(self.level_and_section) + ")"
        return self.user.get_full_name

    @property
    def enrollment_admission_link(self):
        return reverse(
            "administrator:enrollment_admission",
            args=[self.user.id, self.user.get_full_name]
        )


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile")
    civil_status = models.CharField(
        max_length=25, choices=CIVIL_STATUS_CHOICES, default='single')
    spouse = models.CharField(max_length=50, null=True,
                              blank=True, help_text="If Applicable", default='N/A')
    position = models.CharField(max_length=200, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Staff Profile"

    def __str__(self):
        return self.user.get_full_name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    # storage=gd_storage
    photo = models.ImageField(
        upload_to='user/profile/%Y/%m/%d/',
        blank=True, null=True,
    )
    age = models.CharField(max_length=3, blank=True, default='')
    phone_number = models.CharField(
        validators=[phone_regex, ],
        max_length=15,
        blank=True, default='',
        help_text="Please use the format: 0999-999-9999"
    )

    class Meta:
        ordering = ('user__email', )
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return self.user.get_full_name


@receiver(post_save, sender=User)
def create_dynamic_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
        if kwargs['instance'].is_student:
            StudentProfile.objects.create(user=kwargs['instance'])
        elif kwargs['instance'].is_teacher:
            FacultyProfile.objects.create(user=kwargs['instance'])
        elif kwargs['instance'].is_staff:
            StaffProfile.objects.create(user=kwargs['instance'])


@receiver(post_save, sender=Level)
def create_level_slug(sender, **kwargs):
    if kwargs['created']:
        kwargs['instance'].slug = slugify(
            kwargs['instance'].level + " " + str(kwargs['instance'].date_created))
        kwargs['instance'].save()
