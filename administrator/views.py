from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegistrationForm, UserEditForm
from django.contrib.auth.models import Group, User
from django.contrib import messages
from account.models import StudentProfile, StaffProfile, FacultyProfile
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
# Create your views here.


@login_required
@permission_required('auth.add_user', raise_exception=True)
def create_user_done(request):
	return render(request, 'create_user_done.html', {})


@login_required
@permission_required('auth.add_user', raise_exception=True)
def create_user(request):
	if request.method == 'GET':
		form = UserRegistrationForm()
		return render(request, 'create_user.html', {'form': form})
	elif request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password1'])
			new_user.save()
			target_group = Group.objects.get(name=cleaned_data['account'])
			target_group.user_set.add(new_user)
			if cleaned_data['account'] == 'student':
				StudentProfile.objects.create(user=new_user, account=target_group)
			elif cleaned_data['account'] == 'faculty':
				FacultyProfile.objects.create(user=new_user, account=target_group)
			elif cleaned_data['account'] == 'staff':
				StaffProfile.objects.create(user=new_user, account=target_group)
			return HttpResponseRedirect(reverse('administrator:create_user_done'))
		else:
			return HttpResponseRedirect(reverse('administrator:create_user'))


class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = ('auth.add_user', 'auth.delete_user')
	form_class = UserRegistrationForm
	template_name = 'create_user.html'


@login_required
@permission_required('auth.delete_user', raise_exception=True)
def view_users(request):
	users = User.objects.exclude(is_superuser=True)
	return render(request, 'view_users.html', {'users': users})


@login_required
@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, user_id):
	instance = get_object_or_404(User, id=user_id)
	instance.delete()
	return HttpResponseRedirect(reverse('administrator:view_users'))


@login_required
@permission_required('auth.delete_user', raise_exception=True)
def edit_user(request, user_id):
	user_instance = get_object_or_404(User, id=user_id)
	if request.method == 'GET':
		form = UserEditForm(instance=user_instance)
	elif request.method == 'POST':
		form = UserEditForm(request.POST or None, instance=user_instance)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('administrator:edit_user', kwargs={'user_id': user_id}))
	context = {'form': form}
	return render(request, 'edit_user.html', context)