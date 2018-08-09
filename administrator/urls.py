from django.urls import path
from . import views
# Create your forms here


app_name = "administrator"

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
]