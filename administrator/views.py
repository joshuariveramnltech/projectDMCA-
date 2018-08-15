from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from account import forms
from account.models import Profile, LevelAndSection
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


User = get_user_model()

@login_required
def create_user_done(request):
	if not request.user.is_staff:
		raise PermissionDenied
	return render(request, 'create_user_done.html', {'request': request})


@login_required
def create_user(request):
	if not request.user.is_staff:
		raise PermissionDenied

	if request.method == 'GET':
		user_form = forms.UserCreationForm()
	elif request.method == 'POST':
		user_form = forms.UserCreationForm(data=request.POST)
		if user_form.is_valid():
			cleaned_data = user_form.cleaned_data
			new_user = user_form.save(commit=False)
			new_user.set_password(cleaned_data['password1'])
			new_user.save()
			if new_user.is_student:
				Profile.objects.create(user=new_user)
			elif new_user.is_teacher:
				Profile.objects.create(user=new_user)
			return HttpResponseRedirect(reverse('administrator:create_user_done'))
	context = {'user_form': user_form}
	return render(request, 'create_user.html', context)

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
	user_instance = get_object_or_404(User, id=user_id)
	if request.method == 'GET':
		user_form = forms.UserChangeForm(instance=user_instance)
		profile_form = forms.ProfileChangeForm(instance=user_instance.profile)
		level_section_form = forms.LevelAndSectionForm()
	elif request.method == 'POST':
		user_form = forms.UserChangeForm(data=request.POST, instance=user_instance)
		profile_form = forms.ProfileChangeForm(data=request.POST, instance=user_instance.profile, files=request.FILES)
		level_section_form = forms.LevelAndSectionForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return HttpResponseRedirect(reverse('administrator:view_users'))

		if level_section_form.is_valid():
			level_section_form.save()
			return HttpResponseRedirect(reverse('administrator:edit_user', kwargs={'user_id': user_id}))

	context = {
		'user_form': user_form,
		'profile_form': profile_form,
		'level_section_form': level_section_form
		}

	return render(request, 'edit_user.html', context)

@login_required
def create_level_section(request):
	if not request.user.is_staff:
		raise PermissionDenied
	
	if request.method == 'GET':
		level_section_create = forms.LevelAndSectionForm()
	elif request.method == 'POST':
		level_section_create = forms.LevelAndSectionForm(data=request.POST)
		if level_section_create.is_valid():
			level_section_create.save()
			return HttpResponseRedirect(reverse('administrator:view_level_section'))
	return render(request, 'create_level_section.html', {'level_section_create': level_section_create})

@login_required
def view_level_section(request):
	if not request.user.is_staff:
		raise PermissionDenied
	
	level_section = LevelAndSection.objects.all()
	if request.method == 'POST':
		level_section_form = forms.LevelAndSectionForm(data=request.POST)
		if level_section_form.is_valid():
			level_section_form.save()
			return HttpResponseRedirect(reverse('administrator:view_users'))
	context = {'level_section': level_section}

	return render(request, 'view_level_section.html', context)

@login_required
def delete_level_section(request, level_section_id):
	if not request.user.is_staff:
		raise PermissionDenied	
	level_section = LevelAndSection.objects.get(id=level_section_id)
	level_section.delete()
	return HttpResponseRedirect(reverse('administrator:view_level_section'))

@login_required
def edit_level_section(request, level_section_id):
	if not request.user.is_staff:
		raise PermissionDenied
	level_section = get_object_or_404(LevelAndSection, id=level_section_id)
	if request.method == 'GET':
		level_section_edit = forms.LevelAndSectionForm(instance=level_section)
	elif request.method == 'POST':
		level_section_edit = forms.LevelAndSectionForm(data=request.POST, instance=level_section)
		if level_section_edit.is_valid():
			level_section_edit.save()
			return HttpResponseRedirect(reverse('administrator:view_level_section'))
	context =  {'level_section_edit': level_section_edit, 'level_section': level_section}
	return render(request, 'edit_level_section.html', context)