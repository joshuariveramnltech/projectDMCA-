from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from . import forms
from django.contrib import messages
from .models import Announcement
from django.utils import timezone
from django.contrib import messages
# Create your views here.

User = get_user_model()


@login_required
def view_announcement(request):
    dmca_announcement = Announcement.objects.filter(
        send_to_all=True, status='published', publish_date__lte=timezone.now()).order_by('-publish_date')
    try:
        group_announcement = Announcement.objects.filter(
            send_to_group=request.user.profile.level_and_section,
            status='published', publish_date__lte=timezone.now()).exclude(send_to_all=True).order_by('-publish_date')
        context = {
            'request': request,
            'dmca_announcement': dmca_announcement,
            'group_announcement': group_announcement
        }
    except Announcement.DoesNotExist:
        context = {'request': request, 'dmca_announcement': dmca_announcement}
    return render(request, 'view_announcement.html', context)


@login_required
def view_announcement_detail(request, a_id, a_slug):
    announcement = Announcement.objects.get(id=a_id, slug=a_slug)
    context = {'announcement': announcement}
    return render(request, 'announcement_detail.html', context)


@login_required
def create_announcement(request):
    if request.user.is_student:
        raise PermissionDenied
    if request.method == 'GET':
        create_announcement_form = forms.AnnouncementForm()
    elif request.method == 'POST':
        create_announcement_form = forms.AnnouncementForm(data=request.POST)
        if create_announcement_form.is_valid():
            new_announcement = create_announcement_form.save(commit=False)
            new_announcement.author = request.user
            new_announcement.save()
            return HttpResponseRedirect(reverse('announcement:view_announcement'))
    context = {'create_announcement_form': create_announcement_form,
               'request': request}
    return render(request, 'create_announcement.html', context)


@login_required
def edit_announcement(request, a_id, a_slug):
    announcement = Announcement.objects.get(id=a_id, slug=a_slug)
    if request.user.is_student or announcement.author != request.user:
        raise PermissionDenied
    if request.method == 'GET':
        announcement_edit_form = forms.AnnouncementForm(instance=announcement)
    elif request.method == 'POST':
        announcement_edit_form = forms.AnnouncementForm(
            data=request.POST, instance=announcement)
        if announcement_edit_form.is_valid():
            announcement_edit_form.save()
            messages.success(request, 'Your Announcement was updated.')
            return HttpResponseRedirect(announcement.get_absolute_url_for_edit)
    context = {'announcement_edit_form': announcement_edit_form,
               'announcement': announcement}
    return render(request, 'edit_announcement.html', context)


@login_required
def draft_announcement(request):
    if request.user.is_student:
        raise PermissionDenied
    draft_announcement = Announcement.objects.filter(
        status='draft', author=request.user)
    context = {'draft_announcement': draft_announcement}
    return render(request, 'draft_announcement.html', context)


@login_required
def delete_announcement(request, a_id, a_slug):
    announcement = Announcement.objects.get(id=a_id, slug=a_slug)
    if request.user.is_student or request.user != announcement.author:
        raise PermissionDenied
    announcement.delete()
    return HttpResponseRedirect(reverse('announcement:view_announcement'))
