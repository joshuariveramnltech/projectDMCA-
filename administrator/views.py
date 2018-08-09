from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Profile
# Create your views here.


@login_required
def create_user(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            target_group = Group.objects.get(name=form.cleaned_data['account_type'])
            target_group.user_set.add(new_user)
            Profile.objects.create(user=new_user)
        else:
            messages.error(request, 'Error updating your Profile')
            return HttpResponse('User Created Succesfully')
    return render(request, 'create_user.html', {'form': form})


