from django.urls import path
from . import views
# Create your forms here


app_name = "administrator"

urlpatterns = [
    path('create_student/', views.create_student, name='create_user'),

]