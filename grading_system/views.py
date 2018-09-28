from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Subject, SubjectGrade, FinalGrade
from account.models import (
    StudentProfile, StaffProfile, FacultyProfile, LevelAndSection)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from datetime import datetime
from .forms import SubjectGradeEditForm
# Create your views here.

User = get_user_model()


# for faculty account
@login_required
def view_students_per_subject(request, level_section_id, subject_id):
    if not request.user.is_teacher:
        raise PermissionDenied
    context = {'request': request}
    year_section = LevelAndSection.objects.get(id=level_section_id)
    subject = Subject.objects.get(id=subject_id)
    yearSectionStudents_list = StudentProfile.objects.filter(
        level_and_section=level_section_id).order_by('-date_created')
    enrolledStudentsPerSubject_list = SubjectGrade.objects.filter(
        subject=subject_id,
        school_year=str(datetime.now().year)+"-"+str(datetime.now().year+1),
        instructor=request.user.faculty_profile.id
    ).order_by('-date_created')
    yearSection_query = request.GET.get("yearSection_query")
    enrolledStudent_query = request.GET.get("enrolledStudent_query")
    if yearSection_query:
        yearSectionStudents_list = yearSectionStudents_list.filter(
            Q(user__first_name__icontains=yearSection_query) |
            Q(user__last_name__icontains=yearSection_query) |
            Q(user__middle_name__icontains=yearSection_query) |
            Q(user__email__icontains=yearSection_query)).distinct()
    if enrolledStudent_query:
        enrolledStudentsPerSubject_list = enrolledStudentsPerSubject_list.filter(
            Q(student__user__first_name__icontains=enrolledStudent_query) |
            Q(student__user__last_name__icontains=enrolledStudent_query) |
            Q(student__user__middle_name__icontains=enrolledStudent_query) |
            Q(student__user__email__icontains=enrolledStudent_query)).distinct()

    yearSection_paginator = Paginator(yearSectionStudents_list, 20)
    yearSection_page = request.GET.get('yearSection_page')
    try:
        yearSectionStudents = yearSection_paginator.page(yearSection_page)
    except PageNotAnInteger:
        yearSectionStudents = yearSection_paginator.page(1)
    except EmptyPage:
        yearSectionStudents = yearSection_paginator.page(
            yearSection_paginator.num_pages)

    enrolledStudent_paginator = Paginator(enrolledStudentsPerSubject_list, 20)
    enrolledStudent_page = request.GET.get('enrolledStudent_page')
    try:
        enrolledStudentsPerSubject = enrolledStudent_paginator.page(
            enrolledStudent_page)
    except PageNotAnInteger:
        enrolledStudentsPerSubject = enrolledStudent_paginator.page(1)
    except EmptyPage:
        enrolledStudentsPerSubject = enrolledStudent_paginator.page(
            enrolledStudent_paginator.num_pages)
    context.update(
        {'yearSectionStudents': yearSectionStudents,
         'enrolledStudentsPerSubject': enrolledStudentsPerSubject,
         'year_section': year_section,
         'subject': subject
         })
    return render(request, 'view_students_per_subject.html', context)


# for faculty account
@login_required
def edit_student_subjectGrade(request, user_id, user_full_name, subject_grade_id):
    if not request.user.is_teacher:
        raise PermissionDenied
    student_user = User.objects.get(id=user_id)
    level_and_section = LevelAndSection.objects.get(
        id=student_user.student_profile.level_and_section.id)
    subjectGrade = SubjectGrade.objects.get(id=subject_grade_id)
    context = {
        'student_user': student_user,
        'request': request,
        'subjectGrade': subjectGrade,
        'level_and_section': level_and_section
    }
    if request.method == 'GET':
        subjectGrade_edit_form = SubjectGradeEditForm(instance=subjectGrade)
        context['subjectGrade_edit_form'] = subjectGrade_edit_form
        print(subjectGrade_edit_form)
    elif request.method == 'POST':
        subjectGrade_edit_form = SubjectGradeEditForm(
            data=request.POST,
            instance=subjectGrade
        )
        if subjectGrade_edit_form.is_valid():
            subjectGrade_edit_form.save()
            messages.success(request, 'Subject Grade Updated Successfully!')
            return HttpResponseRedirect(reverse(
                'grading_system:edit_student_subjectGrade',
                args=[user_id, user_full_name, subject_grade_id])
            )
    return render(request, 'edit_student_subjectGrade.html', context)


# for student account
@login_required
def view_subjectGrade(request):
    if not request.user.is_student:
        raise PermissionDenied


# for student account
@login_required
def student_level_section_subject(request, student_level, student_section):
    context = {'request': request}
    if not request.user.is_student:
        raise PermissionDenied
    if student_level and student_section:
        subjects = Subject.objects.filter(
            level_and_section__level__level=student_level,
            level_and_section__section=student_section)
        context['subjects'] = subjects
    return render(request, 'view_student_subject.html', context)


# for faculty account
@login_required
def view_assigned_subject(request):
    context = {'request': request}
    if not request.user.is_teacher:
        raise PermissionDenied
    assigned_subjects = Subject.objects.filter(
        designated_instructor=request.user.faculty_profile)
    context['assigned_subjects'] = assigned_subjects

    return render(request, 'view_assigned_subject.html', context)


# for faculty account only
@login_required
def view_student_profile(request, user_id, short_name):
    context = {'request': request}
    if not request.user.is_teacher:
        raise PermissionDenied
    user = User.objects.get(id=user_id)
    context['other_user'] = user
    return render(request, 'view_user_profile.html', context)


# for student account only
@login_required
def view_faculty_profile(request, user_id, short_name):
    if not request.user.is_student:
        raise PermissionDenied
    context = {'request': request}
    user = User.objects.get(id=user_id)
    context['other_user'] = user
    return render(request, 'view_user_profile.html', context)


# for faculty account only
@login_required
def edit_student_finalLevelGrade(request, user_id, level_id):
    student_user = User.objects.get(id=user_id)
    level_and_section = LevelAndSection.objects.get(
        id=student_user.student_profile.level_and_section.level.id)
    if not request.user.is_teacher and level_and_section.adviser != request.user.faculty_profile:
        raise PermissionDenied
    year_level_subjects = SubjectGrade.objects.filter(
        student=student_user.student_profile,
        subject__level_and_section__level=student_user.student_profile.level_and_section.level,
        school_year=str(datetime.now().year) + "-" +
        str(datetime.now().year+1),
    )
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

    context = {
        'request': request,
        'level_and_section': level_and_section,
        'year_level_subjects': year_level_subjects,
    }

    return render(request, '', context)
