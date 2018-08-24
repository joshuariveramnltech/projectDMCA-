from django.urls import path
from . import views
app_name = 'announcement'

urlpatterns = [
    path('dmca/view/announcement/', views.view_announcement, name='view_announcement'),
    path('dmca/view/announcement/detail/<int:a_id>/<slug:a_slug>/', views.view_announcement_detail, name='view_announcement_detail'),
    path('dmca/edit/announcement/<int:a_id>/<slug:a_slug>/', views.edit_announcement, name='edit_announcement'),
    path('dmca/create/announcement/', views.create_announcement, name='create_announcement'),
    path('dmca/view/edit/draft/announcement/', views.draft_announcement, name='draft_announcement'),
]
