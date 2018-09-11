from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views


app_name = "account"

urlpatterns = [
    path('account/', views.dashboard, name='dashboard'),
    path('account/view/edit/profile/',
         views.view_edit_profile, name='view_edit_profile'),
    path('accounts/change_password/',
         views.change_password, name='change_password'),
]
