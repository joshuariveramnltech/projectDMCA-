from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from account.forms import UserCreationForm, UserChangeForm, ProfileChangeForm
from account.models import Profile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.


User = get_user_model()

@login_required
def create_user_done(request):
	if not request.user.is_staff:
		raise PermissionDenied		
	return render(request, 'create_user_done.html', {})


@login_required
def create_user(request):
	if not request.user.is_staff:
		raise PermissionDenied

	if request.method == 'GET':
		form = UserCreationForm()
	elif request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			new_user = form.save(commit=False)
			new_user.set_password(cleaned_data['password1'])
			new_user.save()
			Profile.objects.create(user=new_user)
			return HttpResponseRedirect(reverse('administrator:create_user_done'))
			
	return render(request, 'create_user.html', {'form': form})

@login_required
def view_users(request):
	if not request.user.is_staff:
		raise PermissionDenied
	users = User.objects.all().exclude(is_superuser=True)
	return render(request, 'view_users.html', {'users': users})


@login_required
def delete_user(request, user_id):
	if not request.user.is_staff:
		raise PermissionDenied
	instance = get_object_or_404(User, id=user_id)
	instance.delete()
	return HttpResponseRedirect(reverse('administrator:view_users'))


@login_required
def edit_user(request, user_id):
	if not request.user.is_staff:
		raise PermissionDenied
	user_instance = User.objects.get(id=user_id)
	if request.method == 'GET':
		user_form = UserChangeForm(instance=user_instance)
		profile_form = ProfileChangeForm(instance=user_instance.profile)
	elif request.method == 'POST':
		user_form = UserChangeForm(data=request.POST, instance=user_instance)
		profile_form = ProfileChangeForm(data=request.POST, instance=user_instance.profile, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return HttpResponseRedirect(reverse('administrator:view_users'))
	context = {'user_form': user_form, 'profile_form': profile_form}

	return render(request, 'edit_user.html', context)
