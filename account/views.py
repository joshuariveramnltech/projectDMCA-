from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})


@login_required
def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return HttpResponse("User Created")

    return render(request, 'register.html', {'form': form})