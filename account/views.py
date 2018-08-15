from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect


User = get_user_model()

# Create your views here.


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    user = get_object_or_404(User, email=request.user.email)
    return render(request, 'dashboard.html', {'user': user})
