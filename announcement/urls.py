from django.urls import path
from . import views
app_name = 'announcement'

urlpatterns = [
    path('dmca/view/announcement/', views.view_announcement, name='view_announcement'),
    # path('dmca/create/announcement/', views.create_announcement, name='create_announcement'),
]
