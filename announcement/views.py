from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def view_announcement(request):
    return render(request, 'view_announcement.html', {})