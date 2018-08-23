from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

@login_required
def view_announcement(request):
    return render(request, 'view_announcement.html', {})


@login_required
def create_announcement(request):
    if request.is_student:
        raise PermissionDenied
    
    return render(request, 'create_announcement.html',{})