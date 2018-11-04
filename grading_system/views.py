from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Subject, SubjectGrade, FinalGrade
from account.models import LevelAndSection, StudentProfile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from datetime import datetime
from .forms import SubjectGradeEditForm, FinalGradeEditForm
# Create your views here.

User = get_user_model()


# for faculty account
@login_required
def view_students_per_subject(request, level_section_id, subject_id):
    current_school_year = str(datetime.now().year) + \
        "-" + str(datetime.now().year + 1)
    if not request.user.is_teacher:
        raise PermissionDenied
    context = {'request': request, 'current_school_year': current_school_year}
    year_section = LevelAndSection.objects.get(id=level_section_id)
    subject = Subject.objects.get(id=subject_id)
    yearSectionStudents_list = StudentProfile.objects.filter(
        level_and_section=level_section_id).order_by('-date_created')
    enrolledStudentsPerSubject_list = SubjectGrade.objects.filter(
        subject=subject_id,
        student__level_and_section__level=subject.level_and_section.level,
        instructor=request.user.faculty_profile.id).order_by('-date_created')
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
def view_assigned_subject(request):
    current_school_year = str(datetime.now().year) + \
        "-" + str(datetime.now().year + 1)
    context = {
        'request': request,
        'current_school_year': current_school_year,
    }
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


# for faculty account
@login_required
def edit_student_subjectgrade(request, user_id, user_full_name, subject_grade_id):
    current_school_year = str(datetime.now().year) + \
        "-" + str(datetime.now().year + 1)
    if not request.user.is_teacher:
        raise PermissionDenied
    student_user = User.objects.get(id=user_id)
    level_and_section = LevelAndSection.objects.get(
        id=student_user.student_profile.level_and_section.id)
    subjectGrade = SubjectGrade.objects.get(id=subject_grade_id)
    if subjectGrade.is_finalized:
        return render(request, 'request_error.html', {})
    context = {
        'student_user': student_user,
        'request': request,
        'subjectGrade': subjectGrade,
        'level_and_section': level_and_section,
        'current_school_year': current_school_year
    }
    if request.method == 'GET':
        subjectGrade_edit_form = SubjectGradeEditForm(instance=subjectGrade)
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
    context['subjectGrade_edit_form'] = subjectGrade_edit_form
    return render(request, 'edit_student_subjectGrade.html', context)


# for faculty account only
@login_required
def edit_student_finalgrade(request, user_id, level_id):
    current_school_year = str(datetime.now().year) + \
        "-" + str(datetime.now().year + 1)
    student_user = User.objects.get(id=user_id)
    level_and_section = LevelAndSection.objects.get(
        id=student_user.student_profile.level_and_section.id)
    if not request.user.is_teacher and level_and_section.adviser.user != request.user:
        raise PermissionDenied
    final_LevelGrade = FinalGrade.objects.get(
        student=student_user.student_profile,
        level=student_user.student_profile.level_and_section.level
    )
    if final_LevelGrade.is_finalized:
        return render(request, 'request_error.html', {})
    year_level_subjects = SubjectGrade.objects.filter(
        student=student_user.student_profile,
        subject__level_and_section__level=student_user.student_profile.level_and_section.level,
    )
    context = {
        'request': request,
        'student_user': student_user,
        'level_and_section': level_and_section,
        'year_level_subjects': year_level_subjects,
        'final_LevelGrade': final_LevelGrade,
        'current_school_year': current_school_year,
    }
    if request.method == 'GET':
        finalGrade_form = FinalGradeEditForm(instance=final_LevelGrade)
    elif request.method == 'POST':
        finalGrade_form = FinalGradeEditForm(
            data=request.POST, instance=final_LevelGrade)
        if finalGrade_form.is_valid():
            finalGrade_form.save()
            messages.success(request, 'Final Grade Updated Successfully!')
            return HttpResponseRedirect(
                reverse('grading_system:edit_student_finalgrade',
                        args=[student_user.id, level_and_section.level.id])
            )
    context['finalGrade_form'] = finalGrade_form
    return render(request, 'edit_student_finalgrade.html', context)


# for faculty account only
@login_required
def view_students_finalgrade(request):
    current_school_year = str(datetime.now().year) + \
        "-" + str(datetime.now().year + 1)
    if not request.user.is_teacher:
        raise PermissionDenied
    student_list = User.objects.filter(
        student_profile__level_and_section__adviser=request.user.faculty_profile,
        student_profile__finalGrade__level__level=request.user.faculty_profile.designated_year_level.level
    ).order_by('-date_created')

    student_query = request.GET.get('student_query')
    if student_query:
        student_list = student_list.filter(
            Q(first_name__icontains=student_query) |
            Q(last_name__icontains=student_query) |
            Q(middle_name__icontains=student_query) |
            Q(email__icontains=student_query) |
            Q(student_profile__level_and_section__level__level__icontains=student_query) |
            Q(student_profile__learner_reference_number__icontains=student_query)
        ).distinct()
    student_paginator = Paginator(student_list, 20)
    student_page = request.GET.get('student_page')
    try:
        students = student_paginator.page(student_page)
    except PageNotAnInteger:
        students = student_paginator.page(1)
    except EmptyPage:
        students = student_paginator.page(student_paginator.num_pages)

    context = {'request': request,
               'students': students, 'current_school_year': current_school_year}
    return render(request, 'view_students_finalgrade.html', context)


# for student account only
@login_required
def view_faculty_profile(request, user_id, short_name):
    if not request.user.is_student:
        raise PermissionDenied
    context = {'request': request}
    user = User.objects.get(id=user_id)
    context['other_user'] = user
    return render(request, 'view_user_profile.html', context)


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


# for student account
@login_required
def view_all_grades(request):
    current_school_year = str(datetime.now().year) + \
        "-" + str(datetime.now().year + 1)
    if not request.user.is_student:
        raise PermissionDenied
    context = {
        'request': request,
        'current_school_year': current_school_year,
        'nursery_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Nursery"
        ),
        'kinder_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Kinder"
        ),
        'grade1_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Grade 1"
        ),
        'grade2_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Grade 2"
        ),
        'grade3_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Grade 3"
        ),
        'grade4_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Grade 4"
        ),
        'grade5_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Grade 5"
        ),
        'grade6_subject_grades': SubjectGrade.objects.filter(
            student=request.user.student_profile,
            subject__level_and_section__level__level="Grade 6"
        ),
        'nursery_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Nursery'
        ).first(),
        'kinder_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Kinder'
        ).first(),
        'grade1_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Grade 1'
        ).first(),
        'grade2_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Grade 2'
        ).first(),
        'grade3_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Grade 3'
        ).first(),
        'grade4_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Grade 4'
        ).first(),
        'grade5_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Grade 5'
        ).first(),
        'grade6_final_grade': FinalGrade.objects.filter(
            student=request.user.student_profile.id,
            level__level='Grade 6'
        ).first(),
    }
    return render(request, 'view_all_grades.html', context)
