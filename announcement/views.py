from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from . import forms
from django.contrib import messages
from .models import Announcement, Comment
from account.models import LevelAndSection
from django.utils import timezone
from datetime import datetime
from django.core.paginator import (PageNotAnInteger, EmptyPage, Paginator)
from django.db.models import Q
# Create your views here.

User = get_user_model()


@login_required
def view_announcement(request):
    school_announcement_list = Announcement.objects.filter(
        send_to_all=True, status='published', publish_date__lte=datetime.now()).order_by('-publish_date')
    school_paginator = Paginator(school_announcement_list, 10)
    school_page = request.GET.get('school_page')
    try:
        school_announcement = school_paginator.page(school_page)
    except PageNotAnInteger:
        school_announcement = school_paginator.page(1)
    except EmptyPage:
        school_announcement = school_paginator.page(school_paginator.num_pages)
    context = {'request': request, 'school_announcement': school_announcement}
    group_announcement_list = []
    group_announcement = level_and_section = None
    if request.user.is_staff:
        group_announcement_list = Announcement.objects.filter(
            send_to_all=False, status='published', author=request.user,
            publish_date__lte=timezone.now()).order_by('-publish_date')
    if request.user.is_student and request.user.student_profile.level_and_section:
        group_announcement_list = Announcement.objects.filter(
            send_to_group=request.user.student_profile.level_and_section,
            status='published',
            publish_date__lte=timezone.now()).order_by('-publish_date')
    elif request.user.is_teacher:
        level_and_section = LevelAndSection.objects.filter(
            adviser=request.user.faculty_profile)
        group_announcement_list = Announcement.objects.filter(
            send_to_group__adviser__user=request.user,
            status='published',
            publish_date__lte=timezone.now()).order_by('-publish_date')
    group_paginator = Paginator(group_announcement_list, 10)
    group_page = request.GET.get('group_page')
    try:
        group_announcement = group_paginator.page(group_page)
    except PageNotAnInteger:
        group_announcement = group_paginator.page(1)
    except EmptyPage:
        group_announcement = group_paginator.page(
            group_paginator.num_pages)
    context.update({'group_announcement': group_announcement,
                    'level_and_section': level_and_section})
    return render(request, 'view_announcement.html', context)


@login_required
def view_announcement_detail(request, a_id, a_slug):
    announcement = Announcement.objects.get(id=a_id, slug=a_slug)
    comment_list = announcement.comments.filter(active=True)
    paginator = Paginator(comment_list, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    if request.method == 'GET':
        comment_form = forms.CommentForm()
    elif request.method == 'POST':
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.announcement = announcement
            new_comment.save()
            return HttpResponseRedirect(reverse('announcement:view_announcement_detail', args=[a_id, a_slug]))
    context = {'announcement': announcement,
               'comment_form': comment_form, 'comments': comments, 'request': request, 'comment_list': comment_list}
    return render(request, 'announcement_detail.html', context)


@login_required
def create_announcement(request):
    if request.user.is_student:
        raise PermissionDenied
    if request.method == 'GET':
        create_announcement_form = forms.AnnouncementForm()
    elif request.method == 'POST':
        create_announcement_form = forms.AnnouncementForm(
            data=request.POST, files=request.FILES)
        if create_announcement_form.is_valid():
            new_announcement = create_announcement_form.save(commit=False)
            new_announcement.author = request.user
            new_announcement.save()
            create_announcement_form.save_m2m()
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
            data=request.POST, instance=announcement, files=request.FILES)
        if announcement_edit_form.is_valid():
            announcement_edit_form.save()
            messages.success(request, 'Your Announcement was updated.')
            return HttpResponseRedirect(announcement.get_absolute_url_for_edit)
    context = {'announcement_edit_form': announcement_edit_form,
               'announcement': announcement}
    return render(request, 'edit_announcement.html', context)


@login_required
def draft_published_announcement(request):
    if request.user.is_student:
        raise PermissionDenied
    draft_announcement_list = Announcement.objects.filter(
        status='draft', author=request.user).order_by('-publish_date')
    draft_announcement_paginator = Paginator(draft_announcement_list, 10)
    draft_page = request.GET.get('draft_page')
    try:
        draft_announcement = draft_announcement_paginator.page(draft_page)
    except PageNotAnInteger:
        draft_announcement = draft_announcement_paginator.page(1)
    except EmptyPage:
        draft_announcement = draft_announcement_paginator.page(
            draft_announcement_paginator.num_pages)
    published_announcement_list = Announcement.objects.filter(
        status='published', author=request.user).order_by('-publish_date')
    published_announcement_paginator = Paginator(
        published_announcement_list, 10)
    published_page = request.GET.get('published_page')
    try:
        published_announcement = published_announcement_paginator.page(
            published_page)
    except PageNotAnInteger:
        published_announcement = published_announcement_paginator.page(1)
    except EmptyPage:
        published_announcement = published_announcement_paginator.page(
            published_announcement_paginator.num_pages)
    context = {'draft_announcement': draft_announcement, 'request': request,
               'published_announcement': published_announcement}
    return render(request, 'draft_published_announcement.html', context)


def created_announcement(request):
    if request.user.is_student:
        raise PermissionDenied
    created_announcements = Announcement.objects.filter(author=request.user)
    context = {'created_announcements': created_announcements,
               'request': request}
    return render(request, 'created_announcement.html', context)


@login_required
def delete_announcement(request, a_id, a_slug):
    announcement = Announcement.objects.get(id=a_id, slug=a_slug)
    if request.user.is_student or request.user != announcement.author:
        raise PermissionDenied
    announcement.delete()
    return HttpResponseRedirect(reverse('announcement:view_announcement'))


@login_required
def delete_comment(request, a_id, a_slug, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(reverse('announcement:view_announcement_detail', args=[a_id, a_slug]))


@login_required
def edit_comment(request, a_id, a_slug, comment_id):
    comment_instance = Comment.objects.get(
        id=comment_id, announcement__id=a_id, announcement__slug=a_slug)
    if request.method == 'GET':
        edit_comment_form = forms.EditCommentForm(instance=comment_instance)
    elif request.method == 'POST':
        edit_comment_form = forms.EditCommentForm(
            instance=comment_instance, data=request.POST)
        if edit_comment_form.is_valid():
            edit_comment_form.save()
            redirect_to = reverse(
                'announcement:view_announcement_detail', args=[a_id, a_slug])
            return redirect(redirect_to)
    context = {'edit_comment_form': edit_comment_form,
               'comment_instance': comment_instance}
    return render(request, 'edit_comment.html', context)


@login_required
def view_user_profile_comment(request, target_user_id, target_user_short_name, a_id):
    announcement = Announcement.objects.get(id=a_id)
    target_user = User.objects.get(id=target_user_id)
    context = {'request': request, 'target_user': target_user,
               'announcement': announcement}
    return render(request, 'view_user_profile_comment.html', context)
