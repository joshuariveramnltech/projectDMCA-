from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from account import forms
from account.models import LevelAndSection, Level
from admission.models import AppointmentRequest
from administrator.forms import AppointmentRequestFormAdmin
from accounting_transaction.forms import StatementAddForm
from accounting_transaction.models import Statement
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from grading_system.models import Subject, SubjectGrade, FinalGrade
from grading_system.forms import (
    FinalGradeCreateForm, SubjectCreateForm,
    SubjectGradeCreateForm
)
from django.db.models import Q
from datetime import datetime

# Create your views here.

User = get_user_model()


@login_required
def create_user_done(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, 'create_user_done.html', {'request': request})


@login_required
def create_user(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'GET':
        user_form = forms.UserCreationForm()
        profile_form = forms.ProfileCreateForm()
    elif request.method == 'POST':
        user_form = forms.UserCreationForm(data=request.POST)
        profile_form = forms.ProfileCreateForm(
            data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            cleaned_data = user_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.set_password(cleaned_data['password1'])
            new_user.save()  # profile instance is created in post_save signal so no worries
            profile_form = forms.ProfileCreateForm(
                instance=new_user.profile, data=request.POST, files=request.FILES)
            profile_form.save()
            return HttpResponseRedirect(reverse('administrator:create_user_done'))
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'create_user.html', context)


@login_required
def view_users(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    staff_list = User.objects.filter(is_staff=True).order_by('-date_created')
    faculty_list = User.objects.all().filter(
        is_teacher=True).order_by('-date_created')
    student_list = User.objects.filter(
        is_student=True).order_by('-date_created')
    student_query = request.GET.get("student_query")
    faculty_query = request.GET.get("faculty_query")
    staff_query = request.GET.get("staff_query")
    if student_query:
        student_list = student_list.filter(
            Q(first_name__icontains=student_query) |
            Q(last_name__icontains=student_query) |
            Q(middle_name__icontains=student_query) |
            Q(email__icontains=student_query) |
            Q(student_profile__level_and_section__level__level__icontains=student_query) |
            Q(student_profile__learner_reference_number__icontains=student_query)).distinct()
    if faculty_query:
        faculty_list = faculty_list.filter(
            Q(first_name__icontains=faculty_query) |
            Q(last_name__icontains=faculty_query) |
            Q(middle_name__icontains=faculty_query) |
            Q(email__icontains=faculty_query)).distinct()
    if staff_query:
        staff_list = staff_list.filter(
            Q(first_name__icontains=staff_query) |
            Q(last_name__icontains=staff_query) |
            Q(middle_name__icontains=staff_query) |
            Q(email__icontains=staff_query)).distinct()
    # Student Pagination
    student_paginator = Paginator(student_list, 6)
    student_page = request.GET.get('student_page')
    try:
        students = student_paginator.page(student_page)
    except PageNotAnInteger:
        students = student_paginator.page(1)
    except EmptyPage:
        students = student_paginator.page(student_paginator.num_pages)
    # Faculty Pagination
    faculty_paginator = Paginator(faculty_list, 6)
    faculty_page = request.GET.get('faculty_page')
    try:
        faculty = faculty_paginator.page(faculty_page)
    except PageNotAnInteger:
        faculty = faculty_paginator.page(1)
    except EmptyPage:
        faculty = faculty_paginator.page(faculty_paginator.num_pages)
    # Staff Pagination
    staff_paginator = Paginator(staff_list, 6)
    staff_page = request.GET.get('staff_page')
    try:
        staffs = staff_paginator.page(staff_page)
    except PageNotAnInteger:
        staffs = staff_paginator.page(1)
    except EmptyPage:
        staffs = staff_paginator.page(staff_paginator.num_pages)
    context = {'students': students,
               'staffs': staffs, 'faculty': faculty}
    return render(request, 'view_users.html', context)


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    instance = get_object_or_404(User, id=user_id)
    instance.delete()
    return HttpResponseRedirect(reverse('administrator:view_users'))


@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    context = {'request': request}
    user_instance = get_object_or_404(User, id=user_id)
    if request.method == 'GET':
        user_form = forms.UserChangeForm(instance=user_instance)
        profile_form = forms.ProfileCreateForm(instance=user_instance.profile)
        if user_instance.is_student:
            context['dynamic_profile_form'] = forms.StudentProfileAdminForm(
                instance=user_instance.student_profile)
        elif user_instance.is_teacher:
            context['dynamic_profile_form'] = forms.FacultyProfileAdminForm(
                instance=user_instance.faculty_profile)
        elif user_instance.is_staff:
            context['dynamic_profile_form'] = forms.StaffProfileAdminForm(
                instance=user_instance.staff_profile)
    elif request.method == 'POST':
        user_form = forms.UserChangeForm(
            data=request.POST, instance=user_instance)
        profile_form = forms.ProfileCreateForm(
            data=request.POST, instance=user_instance.profile, files=request.FILES)
        if user_instance.is_student:
            dynamic_profile_form = forms.StudentProfileAdminForm(
                data=request.POST, instance=user_instance.student_profile)
        elif user_instance.is_teacher:
            dynamic_profile_form = forms.FacultyProfileAdminForm(
                data=request.POST, instance=user_instance.faculty_profile)
        elif user_instance.is_staff:
            dynamic_profile_form = forms.StaffProfileAdminForm(
                data=request.POST, instance=user_instance.staff_profile)
        context['dynamic_profile_form'] = dynamic_profile_form
        if user_form.is_valid() and profile_form.is_valid() and dynamic_profile_form.is_valid():
            user_form.save()
            profile_form.save()
            dynamic_profile_form.save()
            return HttpResponseRedirect(reverse('administrator:view_users'))
    context.update(
        {'user_form': user_form, 'profile_form': profile_form, 'target_user': user_instance})
    return render(request, 'edit_user.html', context)


@login_required
def view_level_section(request):
    context = {}
    if not request.user.is_superuser:
        raise PermissionDenied
    level_section_list = LevelAndSection.objects.all()
    paginator = Paginator(level_section_list, 10)
    page = request.GET.get('page')
    try:
        level_section = paginator.page(page)
    except PageNotAnInteger:
        level_section = paginator.page(1)
    except EmptyPage:
        level_section = paginator.page(paginator.num_pages)
    context['level_section'] = level_section
    if request.method == 'GET':
        level_section_create_form = forms.LevelAndSectionForm()
    elif request.method == 'POST':
        level_section_create_form = forms.LevelAndSectionForm(
            data=request.POST)
        if level_section_create_form.is_valid():
            level_section_create_form.save()
            return HttpResponseRedirect(reverse('administrator:view_level_section'))
    context['level_section_create_form'] = level_section_create_form
    return render(request, 'view_level_section.html', context)


@login_required
def delete_level_section(request, level_section_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    level_section = LevelAndSection.objects.get(id=level_section_id)
    level_section.delete()
    return HttpResponseRedirect(reverse('administrator:view_level_section'))


@login_required
def edit_level_section(request, level_section_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    level_section = get_object_or_404(LevelAndSection, id=level_section_id)
    if request.method == 'GET':
        level_section_edit = forms.LevelAndSectionForm(instance=level_section)
    elif request.method == 'POST':
        level_section_edit = forms.LevelAndSectionForm(
            data=request.POST, instance=level_section)
        if level_section_edit.is_valid():
            level_section_edit.save()
            return HttpResponseRedirect(reverse('administrator:view_level_section'))
    context = {'level_section_edit': level_section_edit,
               'level_section': level_section}
    return render(request, 'edit_level_section.html', context)


@login_required
def create_subject(request, **kwargs):
    redirection_flag = 0 if len(kwargs) == 0 else kwargs['user_id']
    context = {'request': request}
    if not request.user.is_superuser:
        raise PermissionDenied
    subject_list = Subject.objects.all()
    paginator = Paginator(subject_list, 10)
    page = request.GET.get('page')
    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)
    context['subjects'] = subjects
    if request.method == 'GET':
        context['user_id'] = redirection_flag
        create_subject_form = SubjectCreateForm()
    elif request.method == 'POST':
        create_subject_form = SubjectCreateForm(data=request.POST)
        if create_subject_form.is_valid():
            create_subject_form.save()
            if redirection_flag:
                user = User.objects.get(id=redirection_flag)
                return HttpResponseRedirect(reverse('administrator:enrollment_admission',
                                                    args=[user.id, user.get_full_name]))
            else:
                return HttpResponseRedirect(reverse('administrator:create_subject', args=[0, ]))
    context['create_subject_form'] = create_subject_form
    return render(request, 'create_subject.html', context)


@login_required
def edit_subject(request, **kwargs):
    if not request.user.is_superuser:
        raise PermissionDenied
    subject = Subject.objects.get(slug=kwargs['subject_slug'])
    context = {'request': request, 'subject': subject,
               'user_id': kwargs['user_id']}
    if request.method == 'GET':
        edit_subject_form = SubjectCreateForm(instance=subject)
    elif request.method == 'POST':
        edit_subject_form = SubjectCreateForm(
            data=request.POST, instance=subject)
        if edit_subject_form.is_valid():
            edit_subject_form.save()
            if kwargs['user_id'] == 0:
                return HttpResponseRedirect(
                    reverse('administrator:create_subject', args=[kwargs['user_id'], ]))
            else:
                user = User.objects.get(id=kwargs['user_id'])
                return HttpResponseRedirect(
                    reverse('administrator:enrollment_admission',
                            args=[user.id, user.get_full_name]))
    context['edit_subject_form'] = edit_subject_form
    return render(request, 'edit_subject.html', context)


@login_required
def delete_subject(request, **kwargs):
    if not request.user.is_superuser:
        raise PermissionDenied
    subject = get_object_or_404(Subject, slug=kwargs['subject_slug'])
    subject.delete()
    if kwargs['user_id'] == 0:
        return HttpResponseRedirect(
            reverse('administrator:create_subject', args=[kwargs['user_id'], ]))
    else:
        user = User.objects.get(id=kwargs['user_id'])
        return HttpResponseRedirect(reverse('administrator:enrollment_admission',
                                            args=[user.id, user.get_full_name]))


@login_required
def enrollment_admission_student(request, user_id, user_full_name):
    current_school_year = str(datetime.now().year) + \
                          "-" + str(datetime.now().year + 1)
    context = {}
    if not request.user.is_superuser:
        raise PermissionDenied
    student_user = User.objects.get(id=user_id)
    available_subjects = Subject.objects.all()
    enrolled_subjects = SubjectGrade.objects.filter(
        student__user=student_user).order_by('school_year')
    finalGrades = FinalGrade.objects.filter(
        student__user=student_user).order_by('school_year')
    for_filtering_subjects = Subject.objects.filter(
        subject_grade__student__user=student_user)
    context.update({'available_subjects': available_subjects,
                    'student_user': student_user,
                    'request': request,
                    'enrolled_subjects': enrolled_subjects,
                    'finalGrades': finalGrades,
                    'for_filtering_subjects': for_filtering_subjects})
    if request.method == 'POST':
        subject_list = request.POST.getlist('subjectList')
        if subject_list:
            for each in subject_list:
                each_subject = Subject.objects.get(id=int(each))
                SubjectGrade.objects.create(
                    student=student_user.student_profile,
                    instructor=each_subject.designated_instructor,
                    school_year=current_school_year,
                    subject=each_subject
                )
            FinalGrade.objects.get_or_create(
                student=student_user.student_profile,
                level=student_user.student_profile.level_and_section.level,
                school_year=current_school_year
            )
            return HttpResponseRedirect(
                reverse('administrator:enrollment_admission', args=[user_id, user_full_name]))
    return render(request, 'student_enrollment.html', context)


@login_required
def delete_subject_grade(request, user_id, user_full_name, subject_grade_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    subject_grade_instance = SubjectGrade.objects.get(id=subject_grade_id)
    subject_grade_instance.delete()
    return HttpResponseRedirect(
        reverse('administrator:enrollment_admission',
                args=[user_id, user_full_name]))


@login_required
def edit_subjectGrade_admin(request, user_id, user_full_name, subject_grade_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = User.objects.get(id=user_id)
    context = {'request': request, 'target_user': user}
    subjectGrade = SubjectGrade.objects.get(id=subject_grade_id)
    if request.method == 'GET':
        subjectGrade_edit_form = SubjectGradeCreateForm(instance=subjectGrade)
    elif request.method == 'POST':
        subjectGrade_edit_form = SubjectGradeCreateForm(
            data=request.POST, instance=subjectGrade)
        if subjectGrade_edit_form.is_valid():
            subjectGrade_edit_form.save()
            messages.success(request, 'Subject Grade Updated!')
            return HttpResponseRedirect(
                reverse('administrator:edit_subjectGrade_admin',
                        args=[user_id, user_full_name, subject_grade_id]))
    context.update({
        'subjectGrade_edit_form': subjectGrade_edit_form,
        'subjectGrade': subjectGrade})
    return render(request, 'edit_subjectGrade_admin.html', context)


@login_required
def create_student_finalLevelGradeAdmin(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    context = {'request': request}
    if request.method == 'GET':
        finalGrade_form = FinalGradeCreateForm()
        context['finalGrade_form'] = finalGrade_form
    elif request.method == 'POST':
        finalGrade_form = FinalGradeCreateForm(data=request.POST)
        if finalGrade_form.is_valid():
            new_finalGrade = finalGrade_form.save(commit=False)
            new_finalGrade.save()
            student_user = User.objects.get(id=new_finalGrade.student.user.id)
            return HttpResponseRedirect(reverse(
                'administrator:enrollment_admission',
                args=[student_user.id, student_user.get_full_name]))
    return render(request, 'create_student_finalgrade_admin.html', context)


@login_required
def edit_student_finalLevelGradeAdmin(request, final_grade_id, user_full_name):
    if not request.user.is_superuser:
        raise PermissionDenied
    finalGrade = FinalGrade.objects.get(id=final_grade_id)
    student_user = User.objects.get(id=finalGrade.student.user.id)
    context = {
        'request': request,
        'student_user': student_user,
        'finalGrade': finalGrade
    }
    if request.method == 'GET':
        finalGrade_form = FinalGradeCreateForm(instance=finalGrade)
        context['finalGrade_form'] = finalGrade_form
    elif request.method == 'POST':
        finalGrade_form = FinalGradeCreateForm(
            data=request.POST, instance=finalGrade)
        if finalGrade_form.is_valid():
            finalGrade_form.save()
            messages.success(request, 'Final Year Grade Updated Successfully!')
            return HttpResponseRedirect(
                reverse(
                    'administrator:edit_student_finalLevelGradeAdmin',
                    args=[final_grade_id, user_full_name]
                )
            )
    context['finalGrade_form'] = finalGrade_form
    return render(request, 'edit_student_finalgrade_admin.html', context)


@login_required
def delete_student_finalLevelGradeAdmin(request, final_grade_id, user_full_name):
    if not request.user.is_superuser:
        raise PermissionDenied
    finalGrade = FinalGrade.objects.get(id=final_grade_id)
    student_user = User.objects.get(id=finalGrade.student.user.id)
    finalGrade.delete()
    return HttpResponseRedirect(reverse(
        'administrator:enrollment_admission',
        args=[student_user.id, student_user.get_full_name]))


@login_required
def update_statement_admin(request, statement_id, student_full_name, student_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    student_user = User.objects.get(id=student_id)
    statement_instance = Statement.objects.get(id=statement_id)
    context = {
        'request': request, 'student_user': student_user,
        'statement_instance': statement_instance,
    }
    if request.method == 'GET':
        update_statement_form = StatementAddForm(instance=statement_instance)
    elif request.method == 'POST':
        update_statement_form = StatementAddForm(
            data=request.POST, instance=statement_instance)
        if update_statement_form.is_valid():
            update_statement_form.save()
            messages.success(request, 'Statement Updated Sucessfully')
            return HttpResponseRedirect(
                reverse(
                    'administrator:update_statement_admin',
                    args=[statement_id, student_full_name, student_id]
                )
            )
    context['update_statement_form'] = update_statement_form
    return render(request, 'update_statement.html', context)


@login_required
def delete_statement_admin(request, statement_id, student_full_name, student_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    statement_instance = Statement.objects.get(id=statement_id)
    statement_instance.delete()
    return HttpResponseRedirect(
        reverse(
            'administrator:view_statement_admin',
            args=[student_full_name, student_id]
        )
    )


@login_required
def view_statement_admin(request, user_full_name, user_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    student_user = User.objects.get(id=user_id)
    account_statements = Statement.objects.filter(
        student=student_user.student_profile).order_by('school_year')
    context = {
        'request': request, 'student_user': student_user,
        'account_statements': account_statements,
    }
    if request.method == 'GET':
        add_statement_form = StatementAddForm()
    elif request.method == 'POST':
        add_statement_form = StatementAddForm(data=request.POST)
        if add_statement_form.is_valid():
            new_statement = add_statement_form.save(commit=False)
            new_statement.student = student_user.student_profile
            new_statement.save()
            message = 'New Account Statement Added for {}'.format(
                student_user.get_full_name)
            messages.success(request, message)
            return HttpResponseRedirect(
                reverse(
                    'administrator:view_statement_admin',
                    args=[student_user.get_full_name, student_user.id]
                )
            )
    context['add_statement_form'] = add_statement_form
    return render(request, 'view_statement.html', context)


@login_required
def view_create_year_level(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    year_levels = Level.objects.all()
    context = {'request': request, 'year_levels': year_levels}
    if request.method == 'GET':
        year_level_create_form = forms.LevelForm()
    elif request.method == 'POST':
        year_level_create_form = forms.LevelForm(data=request.POST)
        if year_level_create_form.is_valid():
            year_level_create_form.save()
            messages.success(request, 'New year Level is Added')
            return HttpResponseRedirect(reverse('administrator:view_create_year_level'))
    context['year_level_create_form'] = year_level_create_form
    return render(request, 'view_create_year_level.html', context)


@login_required
def view_appointment_request(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    appointment_requests_list = AppointmentRequest.objects.all().order_by('-date_created')
    appointment_query = request.GET.get('appointment_query')
    if appointment_query:
        appointment_requests_list = appointment_requests_list.filter(
            Q(first_name__icontains=appointment_query) |
            Q(last_name__icontains=appointment_query) |
            Q(middle_name__icontains=appointment_query) |
            Q(slug__icontains=appointment_query) |
            Q(email__icontains=appointment_query)
        ).distinct()
    appointment_request_paginator = Paginator(appointment_requests_list, 6)
    appointment_request_page = request.GET.get('appointment_request_page')
    try:
        appointment_requests = appointment_request_paginator.page(
            appointment_request_page)
    except PageNotAnInteger:
        appointment_requests = appointment_request_paginator.page(1)
    except EmptyPage:
        appointment_requests = appointment_request_paginator.page(
            appointment_request_paginator.num_pages)
    context = {'request': request,
               'appointment_requests': appointment_requests}
    return render(request, 'view_appointment_request.html', context)


@login_required
def update_appointment_request(request, appointment_request_id, appointment_request_slug):
    if not request.user.is_superuser:
        raise PermissionDenied
    appointment_request_instance = AppointmentRequest.objects.get(
        id=appointment_request_id)
    context = {
        'request': request,
        'appointment_request_instance': appointment_request_instance
    }
    if request.method == 'GET':
        update_appointment_request_form = AppointmentRequestFormAdmin(
            instance=appointment_request_instance)
    elif request.method == 'POST':
        update_appointment_request_form = AppointmentRequestFormAdmin(
            data=request.POST, instance=appointment_request_instance)
        if update_appointment_request_form.is_valid():
            update_appointment_request_form.save()
            messages.success(
                request, 'Appointment Request Updated Successfully'
            )
            return HttpResponseRedirect(
                reverse(
                    'administrator:update_appointment_request',
                    args=[appointment_request_id, appointment_request_slug]
                )
            )
    context['update_appointment_request_form'] = update_appointment_request_form
    return render(request, 'update_appointment_request.html', context)


@login_required
def delete_appointment_request(request, appointment_request_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    appointment_request_instance = AppointmentRequest.objects.get(
        id=appointment_request_id)
    appointment_request_instance.delete()
    return HttpResponseRedirect(reverse('administrator:view_appointment_request'))
