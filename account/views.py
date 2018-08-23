from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from .forms import ProfileEditForm
from django.contrib import messages

User = get_user_model()
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    user = get_object_or_404(User, email=request.user.email)
    return render(request, 'dashboard.html', {'user': user})

@login_required
def view_edit_profile(request):
    if request.method == 'GET':
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
    elif request.method == 'POST':
        profile_edit_form = ProfileEditForm(
            data=request.POST, 
            instance=request.user.profile,
            files=request.FILES
            )
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            messages.success(request, 'Your profile was updated.')
            return HttpResponseRedirect(reverse('account:view_edit_profile'))
    context = {'profile_edit_form': profile_edit_form}
    return render(request, 'view_edit_profile.html', context)