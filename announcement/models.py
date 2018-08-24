from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import LevelAndSection
from django.conf import settings
from django.utils.text import slugify
# Create your models here.
User = get_user_model()


class Announcement(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_announcements')
    tags = TaggableManager()
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    body = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    send_to_group = models.ForeignKey(
        LevelAndSection, on_delete=models.CASCADE, 
        related_name='group_announcements', null=True, 
        blank=True
        )
    send_to_all = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "announcement:announcement_detail", 
            args=[
                self.publish_date.year, 
                self.publish_date.month, 
                self.publish_date.day, 
                self.publish_date.slug
            ]
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Announcement, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish_date', )

    def __str__(self):
        return '{} by {}.'.format(self.title, self.author.get_full_name)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_comment', null=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Comment By {} on {}'.format(self.author.get_full_name, self.announcement)