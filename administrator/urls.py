from django.urls import path
from . import views
# Create your forms here


app_name = 'administrator'

urlpatterns = [
    path('dmca/create/user/', views.create_user, name='create_user'),
    path('dmca/create/user/done/', views.create_user_done, name='create_user_done'),
    path('dmca/view/users/', views.view_users, name='view_users'),
    path('dmca/delete/user/<int:user_id>/',
         views.delete_user, name='delete_user'),
    path('dmca/edit/user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dmca/create/level/section/',
         views.create_level_section, name='create_level_section'),
    path('dmca/edit/level/section/<int:level_section_id>',
         views.edit_level_section, name='edit_level_section'),
    path('dmca/view/level/section/',
         views.view_level_section, name='view_level_section'),
    path('dmca/delete/level/section/<int:level_section_id>',
         views.delete_level_section, name='delete_level_section'),
]
