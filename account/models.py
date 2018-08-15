from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings
from django.core.validators import RegexValidator
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email=None, first_name=None, last_name=None, middle_name=None, password=None, is_active=True, is_staff=False, is_superuser=False):
        if email is None:
            raise ValueError("Users must have an email address!")
        if password is None:
            raise ValueError("Users must have a password")
        if first_name is None:
            raise ValueError("Users must have a first name!")
        if last_name is None:
            raise ValueError("Users must have a last name!")

        user = self.model (
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            middle_name = middle_name,
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save(using=self._db)
        return user

    
    def create_staffuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name = first_name,
            last_name = last_name,
            password = password,
            is_staff = True
        )

        return user


    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name = first_name,
            last_name = last_name,
            password = password,
            is_staff = True,
            is_superuser = True

        )

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=u"Active",) # can lagin
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    @property
    def get_full_name(self):
        if self.middle_name is not None:
            full_name = "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
        else:
            full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()


    @property
    def get_short_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.email


class LevelAndSection(models.Model):
    LEVEL_CHOICES = (
        ('nursery', 'Nursery'), ('kinder', 'Kinder'),
        ('grade_1', 'Grade 1'), ('grade_2', 'Grade 2'),
        ('grade_3', 'Grade 3'), ('grade_4', 'Grade 4'),
        ('grade_5', 'Grade 5'), ('grade_6', 'Grade 6')
    )

    level = models.CharField(max_length=25, choices=LEVEL_CHOICES)
    section = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Levels and Sections'


    def __str__(self):
        return "{} {}".format(self.level, self.section)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to='photo/', null=True, blank=True)
    date_of_birth = models.DateField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    level_and_section = models.ForeignKey(LevelAndSection, on_delete=None, blank=True, null=True, related_name="members")
    position = models.CharField(max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Accepted Format:+639999999999.")
    phone_number = models.CharField(validators=[phone_regex, ], max_length=15, blank=True, null=True)


    def __str__(self):
        return self.user.email
