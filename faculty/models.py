from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Announcement(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
        )
    tags = TaggableManager()
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date ='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse("faculty:post_announcement", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title