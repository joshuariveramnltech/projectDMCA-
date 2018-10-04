from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import LevelAndSection
from django.utils.text import slugify
from datetime import datetime
# Create your models here.
User = get_user_model()


class Announcement(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_announcements')
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    body = models.TextField()
    file = models.FileField(
        upload_to='file/announcement/%Y/%m/%d/', blank=True, null=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')
    send_to_group = models.ForeignKey(
        LevelAndSection, on_delete=models.CASCADE,
        related_name='group_announcements', null=True,
        blank=True, verbose_name="Send to what Year and Section"
    )
    send_to_all = models.BooleanField(default=False, verbose_name="Send to all users?")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and self.publish_date is None:
            self.publish_date = datetime.now()
        super(Announcement, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse(
            "announcement:view_announcement_detail",
            args=[self.id, self.slug]
        )

    @property
    def get_absolute_url_for_edit(self):
        return reverse(
            "announcement:edit_announcement",
            args=[self.id, self.slug]
        )

    @property
    def get_absolute_url_for_delete(self):
        return reverse(
            "announcement:delete_announcement",
            args=[self.id, self.slug]
        )

    class Meta:
        ordering = ('-publish_date', )

    def __str__(self):
        return '{} by {}.'.format(self.title, self.author.get_full_name)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='personal_comment', null=True)
    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_created', )

    def __str__(self):
        return 'Comment By {} on {}'.format(self.author.get_full_name, self.announcement)
