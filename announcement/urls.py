from django.urls import path
from . import views


app_name = 'announcement'

urlpatterns = [
    path('dmca/view/announcement/',
         views.view_announcement, name='view_announcement'),
    path('dmca/view/announcement/detail/<int:a_id>/<slug:a_slug>/',
         views.view_announcement_detail, name='view_announcement_detail'),
    path('dmca/edit/announcement/<int:a_id>/<slug:a_slug>/',
         views.edit_announcement, name='edit_announcement'),
    path('dmca/create/announcement/',
         views.create_announcement, name='create_announcement'),
    path('dmca/view/edit/draft/announcement/',
         views.draft_published_announcement, name='draft_published_announcement'),
    path('dmca/delete/announcement/<int:a_id>/<slug:a_slug>/',
         views.delete_announcement, name='delete_announcement'),
    path('dmca/delete/comment/<int:a_id>/<slug:a_slug>/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('dmca/edit/comment/<int:a_id>/<slug:a_slug>/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('dmca/view/comment/profile/<int:target_user_id>/<target_user_short_name>/<int:a_id>/',
         views.view_user_profile_comment, name='view_user_profile_comment'),
    path('dmca/view/all-created/announcement/',
         views.created_announcement, name='created_announcement'),
]
