from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Statement
from django.core.exceptions import PermissionDenied
from account.models import StudentProfile, StaffProfile
from django.contrib.auth import get_user_model
from .forms import StatementCreateForm, StatementAddForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

User = get_user_model()


# staff account only
@login_required
def view_user_list(request):
    context = {'request': request}
    if not request.user.is_staff:
        raise PermissionDenied
    student_list = User.objects.filter(
        is_student=True).order_by('-date_created')
    student_query = request.GET.get("student_query")
    if student_query:
        student_list = student_list.filter(
            Q(first_name__icontains=student_query) |
            Q(last_name__icontains=student_query) |
            Q(middle_name__icontains=student_query) |
            Q(email__icontains=student_query) |
            Q(student_profile__level_and_section__level__level__icontains=student_query) |
            Q(student_profile__learner_reference_number__icontains=student_query)).distinct()
    # Student Pagination
    student_paginator = Paginator(student_list, 20)
    student_page = request.GET.get('student_page')
    try:
        students = student_paginator.page(student_page)
    except PageNotAnInteger:
        students = student_paginator.page(1)
    except EmptyPage:
        students = student_paginator.page(student_paginator.num_pages)
    context['students'] = students
    return render(request, 'view_user_list.html', context)


# staff account only
@login_required
def update_statement(request, statement_id, student_full_name, student_id):
    if not request.user.is_staff:
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
                    'accounting_transaction:update_statement',
                    args=[statement_id, student_full_name, student_id]
                )
            )
    context['update_statement_form'] = update_statement_form
    return render(request, 'update_statement.html', context)


# staff account only
@login_required
def view_statement(request, user_full_name,  user_id):
    if not request.user.is_staff:
        raise PermissionDenied
    student_user = User.objects.get(id=user_id)
    account_statements = Statement.objects.filter(
        student=student_user.student_profile).order_by('school_year')
    context = {
        'request': request, 'student_user': student_user,
        'account_statements': account_statements,
        'account_statements': account_statements
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
                    'accounting_transaction:view_statement',
                    args=[student_user.get_full_name, student_user.id]
                )
            )
    context['add_statement_form'] = add_statement_form
    return render(request, 'view_statement.html', context)


def delete_statement(request, statement_id, student_full_name, student_id):
    if not request.user.is_staff:
        raise PermissionDenied
    statement_instance = Statement.objects.get(id=statement_id)
    statement_instance.delete()
    return HttpResponseRedirect(
        reverse(
            'accounting_transaction:view_statement',
            args=[student_full_name, student_id]
        )
    )


# for student account only
@login_required
def student_view_statement(request):
    if not request.user.is_student:
        raise PermissionDenied
    student_statements = Statement.objects.filter(student__user=request.user)
    statement_paginator = Paginator(student_statements, 10)
    statement_page = request.GET.get('statement_page')
    try:
        statements = statement_paginator.page(statement_page)
    except PageNotAnInteger:
        statements = statement_paginator.page(1)
    except EmptyPage:
        statements = statement_paginator.page(statement_paginator.num_pages)
    context = {'request': request, 'statements': statements}
    return render(request, 'student_view_statement.html', context)
