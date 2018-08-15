from django.urls import path
from . import views
# Create your forms here


app_name = 'administrator'

urlpatterns = [
	path('dmca/create_user/', views.create_user, name='create_user'),
 	path('dmca/create_user/done/', views.create_user_done, name='create_user_done'),
 	path('dmca/view_users/', views.view_users, name='view_users'),
	path('dmca/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
 	path('dmca/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
]
