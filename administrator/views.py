from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateStudentAccount
# Create your views here.


@login_required
def create_student(request):
    pass


@login_required
def create_faculty(request):
    pass


@login_required
def create_staff(request):
    pass


