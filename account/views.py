from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group

# Create your views here.


@login_required
def dashboard(request):
    user = get_object_or_404(User, username=request.user.username)
    return render(request, 'dashboard.html', {'user': user})
