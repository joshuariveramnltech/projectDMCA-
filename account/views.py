from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from .forms import (ProfileEditForm, PersonalForm, StudentPersonalProfileForm,
                    FacultyPersonalProfileForm, StaffPersonalProfileForm)
from django.contrib import messages
from account.models import (Profile, StudentProfile, LevelAndSection,
                            FacultyProfile, StaffProfile)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()
# Create your views here.


@login_required
def dashboard(request):
    context = {'request': request}
    if request.user.is_teacher:
        try:
            level_and_section = LevelAndSection.objects.filter(
                adviser__user__email=request.user.email)
            context['levels_and_sections'] = level_and_section
        except LevelAndSection.DoesNotExist:
            print('No Level and Section Assigned for this Faculty')
    return render(request, 'dashboard.html', context)


@login_required
def view_edit_profile(request):
    context = {'request': request}
    if request.method == 'GET':
        personal_form = PersonalForm(instance=request.user)
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
        context.update({'profile_edit_form': profile_edit_form,
                        'personal_form': personal_form, })
        if request.user.is_student:
            context['dynamic_profile_form'] = StudentPersonalProfileForm(
                instance=request.user.student_profile)
        elif request.user.is_teacher:
            context['dynamic_profile_form'] = FacultyPersonalProfileForm(
                instance=request.user.faculty_profile)
        elif request.user.is_staff:
            context['dynamic_profile_form'] = StaffPersonalProfileForm(
                instance=request.user.staff_profile)
    elif request.method == 'POST':
        personal_form = PersonalForm(data=request.POST, instance=request.user)
        profile_edit_form = ProfileEditForm(
            data=request.POST, instance=request.user.profile, files=request.FILES)
        if request.user.is_student:
            dynamic_profile_form = StudentPersonalProfileForm(
                data=request.POST, instance=request.user.student_profile)
        elif request.user.is_teacher:
            dynamic_profile_form = FacultyPersonalProfileForm(
                data=request.POST, instance=request.user.faculty_profile)
        elif request.user.is_staff:
            dynamic_profile_form = StaffPersonalProfileForm(
                data=request.POST, instance=request.user.staff_profile)
        if profile_edit_form.is_valid() and personal_form.is_valid() and dynamic_profile_form.is_valid():
            personal_form.save()
            profile_edit_form.save()
            dynamic_profile_form.save()
            messages.success(request, 'Your profile was updated.')
            return HttpResponseRedirect(reverse('account:view_edit_profile'))
    return render(request, 'view_edit_profile.html', context)


@login_required
def change_password(request):
    context = {'request': request}
    new_pw = None
    if request.method == "GET":
        form = PasswordChangeForm(request.user)
    elif request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_pw = form.save()
            update_session_auth_hash(request, new_pw)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('account:change_password'))
    context['form'] = form
    return render(request, 'change_password.html', context)
