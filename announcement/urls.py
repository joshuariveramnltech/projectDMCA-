from django.urls import path
from . import views
app_name = 'announcement'

urlpatterns = [
    path('dmca/view/announcement/', views.view_announcement, name='view_announcement'),
]
