from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from .forms import ProfileEditForm, PersonalForm
from django.contrib import messages
from account.models import Profile
User = get_user_model()
# Create your views here.


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    user = get_object_or_404(User, email=request.user.email)
    try:
        profile = Profile.objects.get(user=user)
        teacher = User.objects.get(is_teacher=True, profile__level_and_section=user.profile.level_and_section)
        context = {'user': user, 'teacher': teacher, 'profile': profile}
    except User.DoesNotExist:
        context = {'user': user, 'profile': profile}
    except Profile.DoesNotExist:
        context = {'user': user}
    return render(request, 'dashboard.html', context)


@login_required
def view_edit_profile(request):
    if request.method == 'GET':
        personal_form = PersonalForm(instance=request.user)
        try:
            profile_edit_form = ProfileEditForm(instance=Profile.objects.get(user=request.user))
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
            profile_edit_form = ProfileEditForm(instance=request.user.profile)
    elif request.method == 'POST':
        personal_form = PersonalForm(
            data=request.POST,
            instance=request.user,
            )
        profile_edit_form = ProfileEditForm(
            data=request.POST,
            instance=Profile.objects.get(user=request.user),
            files=request.FILES
            )
        if profile_edit_form.is_valid() and personal_form.is_valid():
            personal_form.save()
            profile_edit_form.save()
            messages.success(request, 'Your profile was updated.')
            return HttpResponseRedirect(reverse('account:view_edit_profile'))
    context = {
        'profile_edit_form': profile_edit_form,
        'personal_form': personal_form,
        'request': request
        }
    return render(request, 'view_edit_profile.html', context)
